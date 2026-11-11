from io import BytesIO
import pandas as pd
from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from app.models.entities import Dataset, TrafficObservation, Site

REQUIRED = {"timestamp", "visitors"}
OPTIONAL = {"sessions", "page_views"}

def parse_csv(content: bytes, timezone_name: str = "UTC") -> pd.DataFrame:
    try: df = pd.read_csv(BytesIO(content))
    except Exception as exc: raise HTTPException(422, f"CSV could not be read: {exc}")
    df.columns = [str(c).strip().lower() for c in df.columns]
    missing = REQUIRED - set(df.columns)
    if missing: raise HTTPException(422, f"Missing required columns: {', '.join(sorted(missing))}")
    unexpected = set(df.columns) - REQUIRED - OPTIONAL
    if unexpected: raise HTTPException(422, f"Unsupported columns: {', '.join(sorted(unexpected))}")
    if df.empty: raise HTTPException(422, "The CSV contains no observations.")
    if df["timestamp"].isna().any(): raise HTTPException(422, "Missing timestamps were found; correct them instead of replacing them with zero.")
    parsed = pd.to_datetime(df["timestamp"], errors="coerce")
    if parsed.isna().any(): raise HTTPException(422, "One or more timestamps are invalid.")
    if parsed.dt.tz is None: parsed = parsed.dt.tz_localize(timezone_name, ambiguous="raise", nonexistent="raise")
    parsed = parsed.dt.tz_convert("UTC")
    df["timestamp"] = parsed
    for col in ["visitors", *OPTIONAL.intersection(df.columns)]:
        if df[col].isna().any(): raise HTTPException(422, f"Missing values found in {col}; missing values are not converted to zero.")
        numeric = pd.to_numeric(df[col], errors="coerce")
        if numeric.isna().any() or (numeric < 0).any() or ((numeric % 1) != 0).any(): raise HTTPException(422, f"{col} must contain non-negative whole numbers.")
        df[col] = numeric.astype("int64")
    if df["timestamp"].duplicated().any(): raise HTTPException(422, "Duplicate timestamps found in this file.")
    df = df.sort_values("timestamp").reset_index(drop=True)
    return df

def import_csv(db: Session, site: Site, filename: str, content: bytes, timezone_name: str):
    df = parse_csv(content, timezone_name)
    incoming = set(df["timestamp"].tolist())
    existing = db.scalars(select(TrafficObservation.timestamp).where(TrafficObservation.site_id == site.id)).all()
    existing_utc = {pd.Timestamp(value).tz_convert("UTC") if pd.Timestamp(value).tzinfo else pd.Timestamp(value, tz="UTC") for value in existing}
    if incoming.intersection(existing_utc):
        raise HTTPException(409, "One or more timestamps already exist for this site. Import overlapping data as a separate site or reconcile the source files first.")
    dataset = Dataset(site_id=site.id, source="csv", filename=filename, timezone_name=timezone_name, row_count=len(df))
    db.add(dataset); db.flush()
    rows = []
    for row in df.to_dict("records"):
        rows.append(TrafficObservation(site_id=site.id, dataset_id=dataset.id, timestamp=row["timestamp"].to_pydatetime(), visitors=int(row["visitors"]), sessions=int(row["sessions"]) if "sessions" in row else None, page_views=int(row["page_views"]) if "page_views" in row else None))
    db.add_all(rows)
    try: db.commit()
    except IntegrityError:
        db.rollback(); raise HTTPException(409, "An observation conflicts with an existing record in this dataset.")
    db.refresh(dataset)
    return dataset

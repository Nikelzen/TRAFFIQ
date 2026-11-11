import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.entities import TrafficObservation

def observations_frame(db: Session, site_id: str) -> pd.DataFrame:
    rows = db.scalars(select(TrafficObservation).where(TrafficObservation.site_id == site_id).order_by(TrafficObservation.timestamp)).all()
    return pd.DataFrame([{"timestamp": r.timestamp, "visitors": r.visitors, "sessions": r.sessions, "page_views": r.page_views} for r in rows])

def summary(df: pd.DataFrame) -> dict:
    if df.empty: return {"available": False, "reason": "No traffic observations are available for this site."}
    v = df["visitors"].astype(float)
    growth = None
    if len(v) >= 2 and v.iloc[0] != 0: growth = (v.iloc[-1] - v.iloc[0]) / v.iloc[0] * 100
    return {"available": True, "observations": int(len(df)), "total_visitors": int(v.sum()), "average_visitors": float(v.mean()), "peak_traffic": int(v.max()), "lowest_traffic": int(v.min()), "growth_percent": growth, "first_timestamp": df.timestamp.min().isoformat(), "last_timestamp": df.timestamp.max().isoformat(), "total_sessions": int(df.sessions.sum()) if "sessions" in df and df.sessions.notna().all() else None, "total_page_views": int(df.page_views.sum()) if "page_views" in df and df.page_views.notna().all() else None}

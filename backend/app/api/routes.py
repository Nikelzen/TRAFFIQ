from datetime import datetime, timezone
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Query
from fastapi.responses import Response
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from app.database.session import get_db
from app.models.entities import Site, Dataset, TrafficObservation, TrackingEvent
from app.schemas.traffic import SiteCreate, SiteOut, TrackingPayload
from app.services.ingestion import import_csv
from app.services.analytics import observations_frame, summary
from app.services.calculus import polynomial_analysis
from app.services.forecasting import evaluate_models, forecast
from app.services.anomalies import detect_anomalies
from app.services.capacity import calculate_capacity
from app.services.reporting import csv_bytes, pdf_summary

router=APIRouter()

def owned_site(db:Session,site_id:str,owner_id:str):
    site=db.scalar(select(Site).where(Site.id==site_id,Site.owner_id==owner_id))
    if not site: raise HTTPException(404,"Site not found for this owner.")
    return site

@router.get('/health')
def health(): return {"status":"ok","service":"TrafficIQ API","time":datetime.now(timezone.utc).isoformat()}

@router.post('/sites',response_model=SiteOut)
def create_site(payload:SiteCreate,db:Session=Depends(get_db)):
    site=Site(**payload.model_dump()); db.add(site); db.commit(); db.refresh(site); return site

@router.get('/sites',response_model=list[SiteOut])
def list_sites(owner_id:str=Query(...),db:Session=Depends(get_db)):
    return list(db.scalars(select(Site).where(Site.owner_id==owner_id).order_by(Site.created_at.desc())).all())

@router.post('/sites/{site_id}/datasets/csv')
async def upload_csv(site_id:str,owner_id:str=Query(...),timezone_name:str=Query('UTC'),file:UploadFile=File(...),db:Session=Depends(get_db)):
    site=owned_site(db,site_id,owner_id)
    if not file.filename or not file.filename.lower().endswith('.csv'): raise HTTPException(415,'Upload a .csv file.')
    content=await file.read(20*1024*1024+1)
    if len(content)>20*1024*1024: raise HTTPException(413,'CSV exceeds the 20 MB upload limit.')
    dataset=import_csv(db,site,file.filename,content,timezone_name)
    return {"dataset_id":dataset.id,"source":dataset.source,"filename":dataset.filename,"row_count":dataset.row_count,"imported_at":dataset.imported_at.isoformat()}

@router.get('/sites/{site_id}/analytics/summary')
def site_summary(site_id:str,owner_id:str=Query(...),db:Session=Depends(get_db)):
    owned_site(db,site_id,owner_id); return summary(observations_frame(db,site_id))

@router.get('/sites/{site_id}/observations')
def site_observations(site_id:str,owner_id:str=Query(...),db:Session=Depends(get_db)):
    owned_site(db,site_id,owner_id); df=observations_frame(db,site_id)
    if df.empty:return {"available":False,"observations":[]}
    return {"available":True,"observations":[{"timestamp":r.timestamp.isoformat(),"visitors":int(r.visitors),"sessions":None if r.sessions is None else int(r.sessions),"page_views":None if r.page_views is None else int(r.page_views)} for r in df.itertuples()]}

@router.get('/sites/{site_id}/calculus')
def calculus(site_id:str,owner_id:str=Query(...),degree:int=Query(2,ge=1,le=5),db:Session=Depends(get_db)):
    owned_site(db,site_id,owner_id); df=observations_frame(db,site_id)
    if len(df)<3:return {"available":False,"reason":"At least 3 observations are required."}
    x=(df.timestamp-df.timestamp.min()).dt.total_seconds().to_numpy()/3600
    try:return {"available":True,**polynomial_analysis(x,df.visitors.to_numpy(),degree)}
    except ValueError as exc:raise HTTPException(422,str(exc))

@router.get('/sites/{site_id}/forecast/evaluation')
def forecast_evaluation(site_id:str,owner_id:str=Query(...),horizon:int=Query(3,ge=1,le=30),db:Session=Depends(get_db)):
    owned_site(db,site_id,owner_id); df=observations_frame(db,site_id); return evaluate_models(df.visitors.to_numpy() if not df.empty else [],horizon)

@router.get('/sites/{site_id}/forecast')
def create_forecast(site_id:str,owner_id:str=Query(...),model:str=Query('naive'),horizon:int=Query(7,ge=1,le=90),db:Session=Depends(get_db)):
    owned_site(db,site_id,owner_id); df=observations_frame(db,site_id); return forecast(df.visitors.to_numpy() if not df.empty else [],model,horizon)

@router.get('/sites/{site_id}/anomalies')
def anomalies(site_id:str,owner_id:str=Query(...),db:Session=Depends(get_db)):
    owned_site(db,site_id,owner_id); return detect_anomalies(observations_frame(db,site_id))

@router.post('/sites/{site_id}/capacity')
def capacity(site_id:str,payload:dict,owner_id:str=Query(...),db:Session=Depends(get_db)):
    owned_site(db,site_id,owner_id); result=forecast(observations_frame(db,site_id).visitors.to_numpy() if not observations_frame(db,site_id).empty else [],payload.get('model','naive'),payload.get('horizon',7))
    if not result.get('available'):return result
    try:return calculate_capacity(result['predictions'],float(payload.get('headroom_percent',20)),payload.get('capacity_limit'))
    except (ValueError,TypeError) as exc:raise HTTPException(422,str(exc))

@router.post('/tracking/{site_id}')
def track(site_id:str,payload:TrackingPayload,db:Session=Depends(get_db)):
    site=db.get(Site,site_id)
    if not site:raise HTTPException(404,'Unknown tracking site.')
    event=TrackingEvent(site_id=site_id,**payload.model_dump())
    db.add(event)
    try:db.commit()
    except IntegrityError:
        db.rollback(); return {"accepted":True,"duplicate":True}
    return {"accepted":True,"duplicate":False}

@router.get('/sites/{site_id}/reports/summary.csv')
def report_csv(site_id:str,owner_id:str=Query(...),db:Session=Depends(get_db)):
    owned_site(db,site_id,owner_id); df=observations_frame(db,site_id); rows=df.astype(object).where(df.notna(),None).to_dict('records') if not df.empty else []
    for r in rows:
        if r.get('timestamp') is not None:r['timestamp']=r['timestamp'].isoformat()
    return Response(csv_bytes(rows),media_type='text/csv',headers={'Content-Disposition':'attachment; filename=traffiq-observations.csv'})

@router.get('/sites/{site_id}/reports/summary.pdf')
def report_pdf(site_id:str,owner_id:str=Query(...),db:Session=Depends(get_db)):
    site=owned_site(db,site_id,owner_id); df=observations_frame(db,site_id); datasets=db.scalars(select(Dataset).where(Dataset.site_id==site_id)).all(); source=', '.join(sorted({d.source for d in datasets})) or 'No source connected'
    content=pdf_summary(site.name,summary(df),source)
    return Response(content,media_type='application/pdf',headers={'Content-Disposition':'attachment; filename=traffiq-summary.pdf'})

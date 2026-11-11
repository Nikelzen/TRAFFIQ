from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.routes import router
from app.database.session import Base, engine
import app.models.entities  # register SQLAlchemy metadata

app=FastAPI(title=settings.app_name,version="0.1.0",description="Real-data website traffic analytics, calculus and forecasting API")
app.add_middleware(CORSMiddleware,allow_origins=settings.cors_origin_list,allow_credentials=False,allow_methods=["GET","POST","DELETE"],allow_headers=["*"])
app.include_router(router,prefix=settings.api_v1_prefix)

@app.on_event("startup")
def startup():
    # Convenient for the SQLite development fallback. PostgreSQL deployments should use Alembic migrations.
    if settings.database_url.startswith('sqlite'):
        Base.metadata.create_all(bind=engine)

import uuid
from datetime import datetime, timezone
from sqlalchemy import String, DateTime, Float, Integer, ForeignKey, UniqueConstraint, Index, JSON, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.session import Base

def now_utc(): return datetime.now(timezone.utc)

class Site(Base):
    __tablename__ = "sites"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String(160), nullable=False)
    domain: Mapped[str | None] = mapped_column(String(255))
    owner_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now_utc, nullable=False)
    datasets: Mapped[list["Dataset"]] = relationship(back_populates="site", cascade="all, delete-orphan")

class Dataset(Base):
    __tablename__ = "datasets"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    site_id: Mapped[str] = mapped_column(ForeignKey("sites.id", ondelete="CASCADE"), index=True)
    source: Mapped[str] = mapped_column(String(32), nullable=False)
    filename: Mapped[str | None] = mapped_column(String(255))
    timezone_name: Mapped[str] = mapped_column(String(80), default="UTC")
    row_count: Mapped[int] = mapped_column(Integer, default=0)
    imported_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now_utc)
    status: Mapped[str] = mapped_column(String(24), default="completed")
    site: Mapped[Site] = relationship(back_populates="datasets")

class TrafficObservation(Base):
    __tablename__ = "traffic_observations"
    __table_args__ = (UniqueConstraint("dataset_id", "timestamp", name="uq_dataset_timestamp"), Index("ix_observation_site_timestamp", "site_id", "timestamp"))
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    site_id: Mapped[str] = mapped_column(ForeignKey("sites.id", ondelete="CASCADE"), index=True)
    dataset_id: Mapped[str] = mapped_column(ForeignKey("datasets.id", ondelete="CASCADE"), index=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    visitors: Mapped[int] = mapped_column(Integer, nullable=False)
    sessions: Mapped[int | None] = mapped_column(Integer)
    page_views: Mapped[int | None] = mapped_column(Integer)

class TrackingEvent(Base):
    __tablename__ = "tracking_events"
    __table_args__ = (UniqueConstraint("event_id", name="uq_tracking_event_id"), Index("ix_tracking_site_time", "site_id", "occurred_at"))
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    event_id: Mapped[str] = mapped_column(String(80), nullable=False)
    site_id: Mapped[str] = mapped_column(ForeignKey("sites.id", ondelete="CASCADE"), index=True)
    event_type: Mapped[str] = mapped_column(String(30), nullable=False)
    page_path: Mapped[str] = mapped_column(String(500), nullable=False)
    referrer_host: Mapped[str | None] = mapped_column(String(255))
    anonymous_session: Mapped[str | None] = mapped_column(String(80))
    occurred_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

class ForecastRun(Base):
    __tablename__ = "forecasts"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    site_id: Mapped[str] = mapped_column(ForeignKey("sites.id", ondelete="CASCADE"), index=True)
    model_name: Mapped[str] = mapped_column(String(80), nullable=False)
    horizon: Mapped[int] = mapped_column(Integer, nullable=False)
    result: Mapped[dict] = mapped_column(JSON, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now_utc)

class ModelEvaluation(Base):
    __tablename__ = "model_evaluations"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    site_id: Mapped[str] = mapped_column(ForeignKey("sites.id", ondelete="CASCADE"), index=True)
    model_name: Mapped[str] = mapped_column(String(80), nullable=False)
    mae: Mapped[float | None] = mapped_column(Float)
    rmse: Mapped[float | None] = mapped_column(Float)
    smape: Mapped[float | None] = mapped_column(Float)
    mape: Mapped[float | None] = mapped_column(Float)
    test_count: Mapped[int] = mapped_column(Integer, nullable=False)

class Anomaly(Base):
    __tablename__ = "anomalies"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    site_id: Mapped[str] = mapped_column(ForeignKey("sites.id", ondelete="CASCADE"), index=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    observed: Mapped[float] = mapped_column(Float, nullable=False)
    expected: Mapped[float] = mapped_column(Float, nullable=False)
    deviation: Mapped[float] = mapped_column(Float, nullable=False)
    method: Mapped[str] = mapped_column(String(60), nullable=False)
    severity: Mapped[str] = mapped_column(String(20), nullable=False)

class CapacityConfiguration(Base):
    __tablename__ = "capacity_configurations"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    site_id: Mapped[str] = mapped_column(ForeignKey("sites.id", ondelete="CASCADE"), index=True)
    capacity_limit: Mapped[float] = mapped_column(Float, nullable=False)
    headroom_percent: Mapped[float] = mapped_column(Float, nullable=False)
    horizon: Mapped[int] = mapped_column(Integer, nullable=False)

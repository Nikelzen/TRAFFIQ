from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

class SiteCreate(BaseModel):
    name: str = Field(min_length=1, max_length=160)
    domain: str | None = Field(default=None, max_length=255)
    owner_id: str = Field(min_length=1, max_length=36, description="Temporary owner identifier; replace with authenticated principal in production")

class SiteOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str; name: str; domain: str | None; owner_id: str

class ObservationOut(BaseModel):
    timestamp: datetime
    visitors: int
    sessions: int | None = None
    page_views: int | None = None

class TrackingPayload(BaseModel):
    event_id: str = Field(min_length=8, max_length=80)
    event_type: str = Field(pattern="^(page_view)$")
    page_path: str = Field(min_length=1, max_length=500)
    referrer_host: str | None = Field(default=None, max_length=255)
    anonymous_session: str | None = Field(default=None, max_length=80)
    occurred_at: datetime

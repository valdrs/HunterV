from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ReconJobResponse(BaseModel):
    id: int
    target_id: int
    job_type: str
    source: str
    status: str
    error: str | None
    created_at: datetime
    started_at: datetime | None
    completed_at: datetime | None

    model_config = ConfigDict(from_attributes=True)
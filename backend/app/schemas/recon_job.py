from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict


class ReconJobStatus(str, Enum):
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class ReconJobResponse(BaseModel):
    id: int
    target_id: int
    job_type: str
    source: str
    status: ReconJobStatus
    error: str | None
    created_at: datetime | None
    started_at: datetime | None
    completed_at: datetime | None

    model_config = ConfigDict(from_attributes=True)
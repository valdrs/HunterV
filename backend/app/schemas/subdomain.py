from datetime import datetime

from pydantic import BaseModel, ConfigDict


class SubdomainCreate(BaseModel):
    hostname: str
    status: str | None = None
    source: str | None = None
    target_id: int


class SubdomainResponse(BaseModel):
    id: int
    hostname: str
    status: str
    source: str | None
    target_id: int
    first_seen: datetime
    last_seen: datetime

    model_config = ConfigDict(from_attributes=True)
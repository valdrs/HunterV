from datetime import datetime
from pydantic import BaseModel, ConfigDict
from app.schemas.subdomain import SubdomainResponse

class TargetCreate(BaseModel):
    name: str
    base_url: str
    program: str | None = None
    platform: str | None = None
    notes: str | None = None


class TargetResponse(BaseModel):
    id: int
    name: str
    base_url: str
    program: str | None
    platform: str | None
    status: str
    notes: str | None
    created_at: datetime
    subdomains: list[SubdomainResponse] = []

    model_config = ConfigDict(from_attributes=True)


class TargetUpdate(BaseModel):
    name: str | None = None
    base_url: str | None = None
    program: str | None = None
    platform: str | None = None
    status: str | None = None
    notes: str | None = None
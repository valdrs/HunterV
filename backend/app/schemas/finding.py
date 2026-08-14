from datetime import datetime

from pydantic import BaseModel, ConfigDict


class FindingCreate(BaseModel):
    title: str
    severity: str | None = None
    description: str | None = None
    status: str | None = None
    target_id: int


class FindingUpdate(BaseModel):
    title: str | None = None
    severity: str | None = None
    description: str | None = None
    status: str | None = None
    target_id: int | None = None


class FindingResponse(BaseModel):
    id: int
    title: str
    severity: str
    description: str | None
    status: str
    target_id: int

    model_config = ConfigDict(from_attributes=True)
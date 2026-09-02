from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AssetResponse(BaseModel):
    id: int
    target_id: int
    subdomain_id: int | None

    hostname: str
    protocol: str
    port: int

    status: str
    source: str | None

    first_seen: datetime
    last_seen: datetime

    model_config = ConfigDict(from_attributes=True)
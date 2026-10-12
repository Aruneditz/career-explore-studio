from datetime import datetime, timezone
from pydantic import BaseModel, Field


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class HealthCheckResponse(BaseModel):
    status: str = Field(..., example="healthy")
    project: str = Field(..., example="CAREER EXPLORE STUDIO")
    version: str = Field(..., example="1.0.0")
    timestamp: datetime = Field(default_factory=utc_now)
    database: str = Field(..., example="connected")


class MessageResponse(BaseModel):
    message: str
    detail: str | None = None

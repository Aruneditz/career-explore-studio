from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class TopicBase(BaseModel):
    title: str
    description: str
    order_index: int = 0
    is_must_know: bool = False
    estimated_minutes: int = 15


class TopicResponse(TopicBase):
    id: int
    skill_id: int
    is_completed: bool = False
    created_at: datetime

    class Config:
        from_attributes = True


class TopicToggleRequest(BaseModel):
    is_completed: Optional[bool] = Field(None, description="Set completion state explicitly or toggle if omitted")


class TopicToggleResponse(BaseModel):
    topic_id: int
    is_completed: bool
    completed_at: Optional[datetime] = None

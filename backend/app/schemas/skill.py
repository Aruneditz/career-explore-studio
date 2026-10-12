from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from app.schemas.topic import TopicResponse


class SkillOverviewResponse(BaseModel):
    id: int
    goal_id: int
    slug: str
    name: str
    category: str
    description: str
    is_technical: bool
    order_index: int

    # Section 12 Overview details
    what_is_it: Optional[str] = None
    why_important: Optional[str] = None
    where_used: Optional[str] = None
    benefits: Optional[str] = None
    challenges: Optional[str] = None
    prerequisites: Optional[str] = None
    career_relevance: Optional[str] = None

    total_topics: int = 0
    must_know_topics: int = 0
    completed_topics: int = 0
    completion_percentage: float = 0.0

    class Config:
        from_attributes = True


class SkillDetailResponse(SkillOverviewResponse):
    topics: List[TopicResponse] = []

    class Config:
        from_attributes = True

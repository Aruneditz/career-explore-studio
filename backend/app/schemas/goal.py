from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class SkillSummary(BaseModel):
    id: int
    goal_id: int
    slug: str
    name: str
    category: str
    description: str
    is_technical: bool
    order_index: int

    class Config:
        from_attributes = True


class GoalBase(BaseModel):
    slug: str
    title: str
    category: str
    description: str
    career_relevance: str
    icon: str = "Target"
    is_active: bool = True


class GoalResponse(GoalBase):
    id: int
    created_at: datetime
    skills: List[SkillSummary] = []

    class Config:
        from_attributes = True


class GoalSelectRequest(BaseModel):
    goal_id: int = Field(..., description="ID of the career goal to set as active")


class UserGoalResponse(BaseModel):
    id: int
    user_id: int
    goal_id: int
    is_active: bool
    selected_at: datetime
    goal: Optional[GoalResponse] = None

    class Config:
        from_attributes = True

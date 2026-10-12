from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class SkillCompletionRequest(BaseModel):
    force: Optional[bool] = Field(
        default=False,
        description="Bypass must-know topic check if explicitly permitted"
    )
    complete_all_topics: Optional[bool] = Field(
        default=False,
        description="Mark all topics in this skill as completed"
    )


class SkillProgressResponse(BaseModel):
    skill_id: int
    skill_name: str
    skill_category: str
    is_technical: bool
    total_topics: int
    completed_topics: int
    must_know_topics: int
    completed_must_know_topics: int
    progress_percentage: int
    is_completed: bool
    completed_at: Optional[datetime] = None
    can_complete: bool
    completion_requirements: str

    class Config:
        from_attributes = True


class OverallGoalProgressResponse(BaseModel):
    goal_id: int
    goal_title: str
    goal_category: str
    total_skills: int
    completed_skills: int
    overall_percentage: int
    skills: List[SkillProgressResponse]

    class Config:
        from_attributes = True

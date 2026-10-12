from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class AchievementBadge(BaseModel):
    id: str
    title: str
    description: str
    icon: str
    is_unlocked: bool
    category: str
    unlocked_at: Optional[datetime] = None


class SkillDashboardSummary(BaseModel):
    skill_id: int
    skill_name: str
    skill_slug: str
    skill_category: str
    order_index: int
    is_technical: bool
    total_topics: int
    completed_topics: int
    progress_percentage: int
    is_completed: bool
    completed_at: Optional[datetime] = None
    evaluation_score: Optional[int] = None
    evaluation_percentage: Optional[int] = None


class ComprehensiveDashboardResponse(BaseModel):
    user_id: int
    user_name: str
    user_email: str
    member_since: datetime
    goal_id: Optional[int] = None
    goal_title: Optional[str] = None
    goal_slug: Optional[str] = None
    goal_category: Optional[str] = None
    goal_description: Optional[str] = None
    total_skills: int
    completed_skills: int
    in_progress_skills: int
    overall_skill_percentage: int
    total_topics: int
    completed_topics: int
    must_know_topics: int
    completed_must_know_topics: int
    topic_percentage: int
    estimated_total_minutes: int
    estimated_completed_minutes: int
    estimated_completed_hours: float
    completed_skill_evaluations: int
    has_overall_evaluation: bool
    overall_eval_score: Optional[int] = None
    overall_eval_percentage: Optional[int] = None
    overall_readiness_level: Optional[str] = None
    total_interview_questions: int = 15
    practiced_interview_questions: int
    interview_progress_percentage: int
    achievements: List[AchievementBadge]
    skills: List[SkillDashboardSummary]

    class Config:
        from_attributes = True

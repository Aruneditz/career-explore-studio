from datetime import datetime
from typing import List, Optional, Dict
from pydantic import BaseModel, Field


class OverallQuestionOption(BaseModel):
    id: str  # "A", "B", "C", "D"
    text: str


class OverallQuestionResponse(BaseModel):
    id: int
    goal_id: int
    question_text: str
    question_type: str
    integrated_skills: List[str]
    options: List[OverallQuestionOption]
    scenario_context: Optional[str] = None
    order_index: int

    class Config:
        from_attributes = True


class OverallEvaluationSubmissionRequest(BaseModel):
    answers: Dict[str, str] = Field(
        ...,
        description="Dictionary mapping question ID (string) to user's selected option key ('A', 'B', 'C', 'D')"
    )


class OverallQuestionResult(BaseModel):
    question_id: int
    question_text: str
    integrated_skills: List[str]
    selected_option: Optional[str] = None
    correct_option: str
    is_correct: bool
    explanation: str


class OverallEvaluationResultResponse(BaseModel):
    id: int
    goal_id: int
    goal_title: str
    score: int
    total_questions: int
    percentage: int
    readiness_level: str  # "Beginner", "Developing", "Interview-Ready", "Advanced / Exceptional"
    readiness_summary: str
    strong_skills: List[str]
    skills_needing_improvement: List[str]
    cross_skill_insights: List[str]
    recommendations: List[str]
    question_breakdown: List[OverallQuestionResult]
    completed_at: datetime

    class Config:
        from_attributes = True

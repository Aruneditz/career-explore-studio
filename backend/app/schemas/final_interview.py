from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class FinalInterviewQuestionResponse(BaseModel):
    id: int
    goal_id: int
    question_number: int  # 1 to 15
    question: str
    category: str  # "Core Fundamentals", "Practical & Scenario-Based", "Advanced & Problem Solving"
    why_asked: str
    interviewer_looking_for: str
    detailed_answer: str
    simple_syntax: Optional[str] = None
    small_example: Optional[str] = None
    code_or_practical_example: Optional[str] = None
    scenario_example: Optional[str] = None
    response_structure_star: str
    what_not_to_say: str
    is_practiced: bool = False
    practiced_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class FinalInterviewPracticeToggleRequest(BaseModel):
    question_id: int
    is_practiced: Optional[bool] = Field(
        None,
        description="Explicit boolean status to set. If omitted, toggles the current state."
    )


class FinalInterviewPracticeStatusResponse(BaseModel):
    goal_id: int
    goal_title: str
    total_questions: int = 15
    practiced_questions: int
    practiced_count: int
    progress_percentage: int
    practiced_question_ids: List[int]


class FinalInterviewHubResponse(BaseModel):
    goal_id: int
    goal_title: str
    total_questions: int = 15
    practiced_count: int
    progress_percentage: int
    practiced_percentage: float = 0.0
    categories: List[str]
    questions: List[FinalInterviewQuestionResponse]

    class Config:
        from_attributes = True

from datetime import datetime
from typing import List, Optional, Dict
from pydantic import BaseModel, Field


class EvaluationOption(BaseModel):
    id: str  # "A", "B", "C", "D"
    text: str


class EvaluationQuestionResponse(BaseModel):
    id: int
    skill_id: int
    question_text: str
    question_type: str  # "conceptual", "practical", "problem_solving", "understanding"
    options: List[EvaluationOption]
    topic_area: Optional[str] = None
    order_index: int

    class Config:
        from_attributes = True


class EvaluationSubmissionRequest(BaseModel):
    answers: Dict[str, str] = Field(
        ...,
        description="Dictionary mapping question ID (string) to user's selected option key ('A', 'B', 'C', 'D')"
    )


class QuestionResult(BaseModel):
    question_id: int
    question_text: str
    selected_option: Optional[str] = None
    correct_option: str
    is_correct: bool
    explanation: str
    topic_area: Optional[str] = None


class EvaluationResultResponse(BaseModel):
    id: int
    skill_id: int
    score: int
    total_questions: int
    percentage: int
    performance_level: str  # "Mastery" (>=80%), "Proficient" (>=60%), "Developing" (<60%)
    strong_areas: List[str]
    weak_areas: List[str]
    feedback_summary: str
    improvement_suggestions: List[str]
    question_breakdown: List[QuestionResult]
    completed_at: datetime

    class Config:
        from_attributes = True

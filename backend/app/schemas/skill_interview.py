from typing import Optional
from pydantic import BaseModel


class SkillInterviewQuestionResponse(BaseModel):
    id: int
    skill_id: int
    question: str
    difficulty: str  # "Basic", "Intermediate", "Advanced"
    category: str  # "Conceptual", "Practical Scenario", "Architecture", etc.
    expected_answer: str
    simple_syntax: Optional[str] = None
    small_example: Optional[str] = None
    explanation: str
    practical_scenario: Optional[str] = None
    tips_for_answering: str
    common_mistakes: str
    order_index: int

    class Config:
        from_attributes = True


class SkillSequenceInfoResponse(BaseModel):
    current_skill_id: int
    current_skill_name: str
    current_skill_slug: str
    goal_id: int
    goal_title: str
    has_next_skill: bool
    next_skill_id: Optional[int] = None
    next_skill_name: Optional[str] = None
    next_skill_slug: Optional[str] = None
    is_last_skill: bool
    total_skills_in_goal: int
    current_skill_index: int  # 1-based index (e.g., 2 of 5)

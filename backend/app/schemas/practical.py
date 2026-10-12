from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class PracticalContentResponse(BaseModel):
    id: int
    skill_id: int
    title: str
    content_type: str  # "code_syntax", "exercise", "scenario", "case_study"
    language: Optional[str] = None
    code_snippet: Optional[str] = None
    explanation: str
    real_world_context: str
    activity_prompt: Optional[str] = None
    solution_or_guide: Optional[str] = None
    order_index: int
    created_at: datetime

    class Config:
        from_attributes = True

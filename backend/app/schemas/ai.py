from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class AIAskRequest(BaseModel):
    prompt: str = Field(..., min_length=1, max_length=1000, description="User's query for career, skill, topic, or interview guidance.")
    skill_id: Optional[int] = Field(None, description="Optional current skill context ID.")
    topic_id: Optional[int] = Field(None, description="Optional current topic context ID.")


class AIAskResponse(BaseModel):
    query: str
    answer: str
    syntax_or_framework: Optional[str] = None
    code_example: Optional[str] = None
    practical_explanation: Optional[str] = None
    ces_recommendation: Optional[str] = None
    context_used: Dict[str, Any] = Field(default_factory=dict)
    suggestions: List[str] = Field(default_factory=list)


class AISuggestionResponse(BaseModel):
    suggestions: List[str]

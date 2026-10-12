from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class CertificateResponse(BaseModel):
    id: int
    certificate_id: str
    certificate_type: str  # "skill" or "goal"
    skill_id: Optional[int] = None
    goal_id: Optional[int] = None
    title: str
    recipient_name: str
    issued_at: datetime
    status: str
    metadata_json: Optional[str] = None
    verification_url: Optional[str] = None

    class Config:
        from_attributes = True


class SkillCertificateChecklist(BaseModel):
    topics_completed: bool
    topics_summary: str
    practical_completed: bool
    practical_summary: str
    evaluation_completed: bool
    evaluation_summary: str
    interview_completed: bool
    interview_summary: str
    overall_completed: bool
    progress_percentage: int


class SkillCertificateStatusResponse(BaseModel):
    skill_id: int
    skill_name: str
    goal_id: Optional[int] = None
    goal_title: Optional[str] = None
    is_unlocked: bool
    status_message: str
    checklist: SkillCertificateChecklist
    certificate: Optional[CertificateResponse] = None


class UserCertificatesListResponse(BaseModel):
    total_earned: int
    certificates: List[CertificateResponse]

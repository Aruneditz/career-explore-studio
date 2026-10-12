from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.certificate import UserCertificate
from app.schemas.certificate import (
    CertificateResponse,
    SkillCertificateStatusResponse,
    UserCertificatesListResponse,
)
from app.services import certificate_service

router = APIRouter(prefix="", tags=["Certificates"])


class StageRecordRequest(BaseModel):
    stage: str  # "practical", "interview"


@router.get("/certificates", response_model=UserCertificatesListResponse)
def get_user_certificates(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retrieve all official certificates earned by the authenticated user.
    """
    return certificate_service.get_all_user_certificates(db, current_user.id)


@router.get("/certificates/{certificate_id}", response_model=CertificateResponse)
def get_user_certificate_by_id(
    certificate_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retrieve a specific certificate by primary key database ID.
    Strictly verifies ownership to prevent unauthorized access across users.
    """
    cert = db.query(UserCertificate).filter(UserCertificate.id == certificate_id).first()
    if not cert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Certificate with ID {certificate_id} not found."
        )
    if cert.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden: You do not have permission to access another user's certificate."
        )
    return cert


@router.get("/certificates/verify/{certificate_id}", response_model=CertificateResponse)
def verify_certificate(
    certificate_id: str,
    db: Session = Depends(get_db)
):
    """
    Public endpoint to verify an official credential by Certificate ID.
    """
    return certificate_service.verify_certificate_by_id(db, certificate_id)


@router.get("/skills/{skill_id}/certificate", response_model=SkillCertificateStatusResponse)
def get_skill_certificate_status(
    skill_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Check if a skill certificate is unlocked, returning granular checklist of learning stages.
    """
    return certificate_service.get_skill_completion_checklist(db, current_user.id, skill_id)


@router.post("/skills/{skill_id}/claim-certificate", response_model=CertificateResponse)
def claim_skill_certificate(
    skill_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Generate and claim the official certificate for a completed skill.
    Strictly enforces genuine completion across all required stages.
    """
    return certificate_service.claim_or_get_skill_certificate(db, current_user.id, skill_id)


@router.post("/skills/{skill_id}/record-stage", response_model=SkillCertificateStatusResponse)
def record_skill_stage(
    skill_id: int,
    request: StageRecordRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Records interaction for a learning stage (e.g. 'practical' or 'interview').
    """
    return certificate_service.mark_skill_stage_interaction(db, current_user.id, skill_id, request.stage)

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.skill_progress import OverallGoalProgressResponse
from app.schemas.dashboard import ComprehensiveDashboardResponse
from app.services import skill_service, dashboard_service

router = APIRouter()


@router.get("/summary", response_model=Optional[OverallGoalProgressResponse])
def get_progress_summary(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get user's overall learning progress across their active goal and all assigned skills (Section 16).
    Protected endpoint.
    """
    progress = skill_service.get_overall_goal_progress(db, user_id=current_user.id)
    return progress


@router.get("/dashboard", response_model=ComprehensiveDashboardResponse)
def get_comprehensive_dashboard(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retrieve unified full-spectrum progress dashboard (skills, topics, evaluations, interview prep, badges).
    Protected endpoint (Phase 12).
    """
    return dashboard_service.get_user_dashboard(db, user_id=current_user.id)

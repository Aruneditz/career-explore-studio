from typing import Optional
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.api.deps import get_current_user, get_optional_current_user
from app.models.user import User
from app.models.goal import Goal
from app.models.user_goal import UserGoalSelection
from app.schemas.final_interview import (
    FinalInterviewQuestionResponse,
    FinalInterviewPracticeToggleRequest,
    FinalInterviewPracticeStatusResponse,
    FinalInterviewHubResponse,
)
from app.services import final_interview_service

router = APIRouter()


def _resolve_goal_id(
    db: Session,
    goal_id: Optional[int],
    user: Optional[User]
) -> int:
    """Helper to resolve target goal ID from query param, active user selection, or default goal."""
    if goal_id:
        goal = db.query(Goal).filter(Goal.id == goal_id).first()
        if goal:
            return goal.id

    if user:
        active_sel = db.query(UserGoalSelection).filter(
            UserGoalSelection.user_id == user.id,
            UserGoalSelection.is_active == True
        ).first()
        if active_sel:
            return active_sel.goal_id

    first_goal = db.query(Goal).order_by(Goal.id.asc()).first()
    if first_goal:
        return first_goal.id

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="No career goals configured in the database."
    )


@router.get("/hub", response_model=FinalInterviewHubResponse)
def get_final_interview_hub_endpoint(
    goal_id: Optional[int] = Query(None, description="Optional goal ID; defaults to user's active goal"),
    current_user: Optional[User] = Depends(get_optional_current_user),
    db: Session = Depends(get_db)
):
    """
    Get the complete capstone interview preparation hub featuring EXACTLY 15 MUST-KNOW
    INTERVIEW QUESTIONS with model answers, explanations, scenarios, tips, traps, and practice status (Sections 21, 22, 23).
    """
    user_id = current_user.id if current_user else None
    resolved_goal_id = _resolve_goal_id(db, goal_id, current_user)
    return final_interview_service.get_final_interview_hub(
        db,
        goal_id=resolved_goal_id,
        user_id=user_id
    )


@router.get("/practice-status", response_model=FinalInterviewPracticeStatusResponse)
def get_practice_status_endpoint(
    goal_id: Optional[int] = Query(None, description="Optional goal ID; defaults to user's active goal"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get current user's practiced interview questions metrics and IDs for a career goal (Section 23).
    Protected endpoint.
    """
    resolved_goal_id = _resolve_goal_id(db, goal_id, current_user)
    return final_interview_service.get_practice_status(
        db,
        user_id=current_user.id,
        goal_id=resolved_goal_id
    )


@router.post("/toggle-practiced", response_model=FinalInterviewQuestionResponse)
def toggle_practice_endpoint(
    request: FinalInterviewPracticeToggleRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Toggle or update the 'Practiced / Understood' status of a final interview question (Section 23).
    Protected endpoint.
    """
    return final_interview_service.toggle_question_practice(
        db,
        user_id=current_user.id,
        request=request
    )

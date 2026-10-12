from typing import List, Optional
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.api.deps import get_current_user, get_optional_current_user
from app.models.user import User
from app.models.goal import Goal
from app.models.user_goal import UserGoalSelection
from app.models.overall_evaluation import UserGoalEvaluation
from app.schemas.overall_evaluation import (
    OverallQuestionResponse,
    OverallEvaluationSubmissionRequest,
    OverallEvaluationResultResponse,
)
from app.services import overall_evaluation_service

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


@router.get("/questions", response_model=List[OverallQuestionResponse])
def get_overall_evaluation_questions_endpoint(
    goal_id: Optional[int] = Query(None, description="Optional goal ID; defaults to user's active goal"),
    current_user: Optional[User] = Depends(get_optional_current_user),
    db: Session = Depends(get_db)
):
    """
    Get cross-skill evaluation questions for a career goal (Section 20).
    Does not expose correct answers.
    """
    resolved_goal_id = _resolve_goal_id(db, goal_id, current_user)
    return overall_evaluation_service.get_goal_overall_questions(db, goal_id=resolved_goal_id)


@router.get("/latest", response_model=Optional[OverallEvaluationResultResponse])
def get_latest_overall_evaluation_endpoint(
    goal_id: Optional[int] = Query(None, description="Optional goal ID; defaults to user's active goal"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get current user's latest overall cross-skill evaluation diagnostic report (Section 20).
    Protected endpoint.
    """
    resolved_goal_id = _resolve_goal_id(db, goal_id, current_user)
    return overall_evaluation_service.get_latest_user_goal_evaluation(
        db,
        user_id=current_user.id,
        goal_id=resolved_goal_id
    )


@router.post("/submit", response_model=OverallEvaluationResultResponse)
def submit_overall_evaluation_endpoint(
    request: OverallEvaluationSubmissionRequest,
    goal_id: Optional[int] = Query(None, description="Optional goal ID; defaults to user's active goal"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Submit cross-skill evaluation answers, calculate readiness rating, evaluate strong/weak skills,
    and persist results in database (Section 20).
    Protected endpoint.
    """
    resolved_goal_id = _resolve_goal_id(db, goal_id, current_user)
    return overall_evaluation_service.submit_goal_overall_evaluation(
        db,
        user_id=current_user.id,
        goal_id=resolved_goal_id,
        request=request
    )


@router.get("/reports/{report_id}", response_model=OverallEvaluationResultResponse)
def get_overall_report_by_id(
    report_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retrieve a specific cross-skill evaluation diagnostic report by database ID.
    Strictly verifies user ownership and prevents unauthorized cross-user access.
    """
    record = db.query(UserGoalEvaluation).filter(UserGoalEvaluation.id == report_id).first()
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Overall evaluation report with ID {report_id} not found."
        )
    if record.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden: You do not have permission to access another user's evaluation report."
        )
    return overall_evaluation_service.get_latest_user_goal_evaluation(
        db,
        user_id=current_user.id,
        goal_id=record.goal_id
    )

from typing import List, Optional
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.goal import GoalResponse, SkillSummary, GoalSelectRequest, UserGoalResponse
from app.services import goal_service

router = APIRouter()


@router.get("", response_model=List[GoalResponse])
def list_goals(db: Session = Depends(get_db)):
    """
    List all available career goals along with their associated skills.
    Public endpoint.
    """
    return goal_service.get_all_goals(db)


@router.get("/current", response_model=Optional[UserGoalResponse])
def get_current_user_goal(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get the currently active selected goal for the authenticated user.
    Protected endpoint.
    """
    selection = goal_service.get_user_active_goal(db, current_user.id)
    return selection


@router.post("/select", response_model=UserGoalResponse, status_code=status.HTTP_200_OK)
def select_active_goal(
    request: GoalSelectRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Set the active career goal for the current user.
    Protected endpoint.
    """
    selection = goal_service.set_user_active_goal(db, current_user.id, request.goal_id)
    return selection


@router.post("/{goal_id}/select", response_model=UserGoalResponse, status_code=status.HTTP_200_OK)
def select_active_goal_by_path(
    goal_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Set the active career goal for the current user via path parameter.
    Protected endpoint.
    """
    selection = goal_service.set_user_active_goal(db, current_user.id, goal_id)
    return selection


@router.get("/{identifier}", response_model=GoalResponse)
def get_goal_details(identifier: str, db: Session = Depends(get_db)):
    """
    Get detailed information about a career goal by numeric ID or slug.
    Public endpoint.
    """
    return goal_service.get_goal_by_id_or_slug(db, identifier)


@router.get("/{goal_id}/skills", response_model=List[SkillSummary])
def get_goal_skills(goal_id: int, db: Session = Depends(get_db)):
    """
    Get all skills belonging to a specific goal in roadmap order.
    Public endpoint.
    """
    return goal_service.get_skills_for_goal(db, goal_id)

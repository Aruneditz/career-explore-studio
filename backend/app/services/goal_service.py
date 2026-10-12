from typing import List, Optional, Union
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.goal import Goal
from app.models.skill import Skill
from app.models.user_goal import UserGoalSelection


def get_all_goals(db: Session) -> List[Goal]:
    """Retrieve all active career goals."""
    return db.query(Goal).filter(Goal.is_active == True).order_by(Goal.id.asc()).all()


def get_goal_by_id_or_slug(db: Session, identifier: Union[int, str]) -> Optional[Goal]:
    """Retrieve a goal by numeric ID or by slug string."""
    if isinstance(identifier, int) or (isinstance(identifier, str) and identifier.isdigit()):
        goal = db.query(Goal).filter(Goal.id == int(identifier)).first()
    else:
        goal = db.query(Goal).filter(Goal.slug == str(identifier)).first()

    if not goal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Goal '{identifier}' not found."
        )
    return goal


def get_skills_for_goal(db: Session, goal_id: int) -> List[Skill]:
    """Retrieve all skills ordered for a specific goal."""
    # Ensure goal exists
    get_goal_by_id_or_slug(db, goal_id)
    return db.query(Skill).filter(Skill.goal_id == goal_id).order_by(Skill.order_index.asc()).all()


def set_user_active_goal(db: Session, user_id: int, goal_id: int) -> UserGoalSelection:
    """
    Set or update the user's active career goal.
    Ensures that only one goal is marked active at a time.
    """
    # Verify goal exists
    goal = get_goal_by_id_or_slug(db, goal_id)

    # Deactivate any previous goal selections for this user
    db.query(UserGoalSelection).filter(
        UserGoalSelection.user_id == user_id,
        UserGoalSelection.is_active == True
    ).update({"is_active": False})

    # Check if a record already exists for this (user_id, goal_id)
    existing = db.query(UserGoalSelection).filter(
        UserGoalSelection.user_id == user_id,
        UserGoalSelection.goal_id == goal.id
    ).first()

    if existing:
        existing.is_active = True
        selection = existing
    else:
        selection = UserGoalSelection(
            user_id=user_id,
            goal_id=goal.id,
            is_active=True
        )
        db.add(selection)

    db.commit()
    db.refresh(selection)
    return selection


def get_user_active_goal(db: Session, user_id: int) -> Optional[UserGoalSelection]:
    """Retrieve the currently active goal selection for a user."""
    return db.query(UserGoalSelection).filter(
        UserGoalSelection.user_id == user_id,
        UserGoalSelection.is_active == True
    ).first()

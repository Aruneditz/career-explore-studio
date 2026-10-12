from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.skill import Skill
from app.models.goal import Goal
from app.models.skill_interview import SkillInterviewQuestion
from app.schemas.skill_interview import (
    SkillInterviewQuestionResponse,
    SkillSequenceInfoResponse,
)


def get_skill_interview_questions(
    db: Session,
    skill_id: int,
    difficulty: Optional[str] = None
) -> List[SkillInterviewQuestionResponse]:
    """
    Retrieve interview preparation questions for a given skill.
    Supports optional difficulty filtering ('Basic', 'Intermediate', 'Advanced').
    """
    skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if not skill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Skill with ID {skill_id} not found."
        )

    query = db.query(SkillInterviewQuestion).filter(
        SkillInterviewQuestion.skill_id == skill_id
    )

    if difficulty and difficulty.lower() != "all":
        # Case-insensitive difficulty match
        query = query.filter(
            SkillInterviewQuestion.difficulty.ilike(difficulty)
        )

    questions = query.order_by(SkillInterviewQuestion.order_index.asc()).all()
    return questions


def get_skill_sequence_progression(
    db: Session,
    skill_id: int
) -> SkillSequenceInfoResponse:
    """
    Determines sequence progression for a skill within its parent goal track.
    Provides next skill info or flags the final capstone preparation transition (Section 19).
    """
    skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if not skill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Skill with ID {skill_id} not found."
        )

    goal = db.query(Goal).filter(Goal.id == skill.goal_id).first()
    if not goal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Parent Goal for skill ID {skill_id} not found."
        )

    skills_in_goal = db.query(Skill).filter(
        Skill.goal_id == goal.id
    ).order_by(Skill.order_index.asc(), Skill.id.asc()).all()

    current_idx = -1
    for i, s in enumerate(skills_in_goal):
        if s.id == skill.id:
            current_idx = i
            break

    if current_idx == -1:
        # Fallback if somehow not found
        current_idx = 0

    total_skills = len(skills_in_goal)
    has_next = current_idx < (total_skills - 1)
    is_last = not has_next

    next_skill = skills_in_goal[current_idx + 1] if has_next else None

    return SkillSequenceInfoResponse(
        current_skill_id=skill.id,
        current_skill_name=skill.name,
        current_skill_slug=skill.slug,
        goal_id=goal.id,
        goal_title=goal.title,
        has_next_skill=has_next,
        next_skill_id=next_skill.id if next_skill else None,
        next_skill_name=next_skill.name if next_skill else None,
        next_skill_slug=next_skill.slug if next_skill else None,
        is_last_skill=is_last,
        total_skills_in_goal=total_skills,
        current_skill_index=current_idx + 1
    )

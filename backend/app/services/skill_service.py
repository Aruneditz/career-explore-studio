from typing import List, Optional, Union
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.skill import Skill
from app.models.topic import Topic
from app.models.topic_progress import UserTopicProgress
from app.models.practical import PracticalContent
from app.models.skill_progress import UserSkillProgress
from app.models.user_goal import UserGoalSelection
from app.models.goal import Goal
from app.schemas.skill import SkillOverviewResponse
from app.schemas.topic import TopicResponse
from app.schemas.practical import PracticalContentResponse
from app.schemas.skill_progress import (
    SkillProgressResponse,
    SkillCompletionRequest,
    OverallGoalProgressResponse,
)


def get_skill_by_id_or_slug(
    db: Session, 
    identifier: Union[int, str], 
    user_id: Optional[int] = None
) -> SkillOverviewResponse:
    """
    Retrieve skill with detailed overview metrics and user topic completion stats.
    """
    if isinstance(identifier, int) or (isinstance(identifier, str) and identifier.isdigit()):
        skill = db.query(Skill).filter(Skill.id == int(identifier)).first()
    else:
        skill = db.query(Skill).filter(Skill.slug == str(identifier)).first()

    if not skill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Skill '{identifier}' not found."
        )

    # Compute topic metrics
    topics = db.query(Topic).filter(Topic.skill_id == skill.id).all()
    total_topics = len(topics)
    must_know_topics = sum(1 for t in topics if t.is_must_know)

    completed_topics = 0
    if user_id and total_topics > 0:
        topic_ids = [t.id for t in topics]
        completed_topics = db.query(UserTopicProgress).filter(
            UserTopicProgress.user_id == user_id,
            UserTopicProgress.topic_id.in_(topic_ids),
            UserTopicProgress.is_completed == True
        ).count()

    completion_percentage = round((completed_topics / total_topics * 100), 1) if total_topics > 0 else 0.0

    return SkillOverviewResponse(
        id=skill.id,
        goal_id=skill.goal_id,
        slug=skill.slug,
        name=skill.name,
        category=skill.category,
        description=skill.description,
        is_technical=skill.is_technical,
        order_index=skill.order_index,
        what_is_it=skill.what_is_it,
        why_important=skill.why_important,
        where_used=skill.where_used,
        benefits=skill.benefits,
        challenges=skill.challenges,
        prerequisites=skill.prerequisites,
        career_relevance=skill.career_relevance,
        total_topics=total_topics,
        must_know_topics=must_know_topics,
        completed_topics=completed_topics,
        completion_percentage=completion_percentage
    )


def get_skill_topics(
    db: Session, 
    skill_id: int, 
    user_id: Optional[int] = None
) -> List[TopicResponse]:
    """
    Retrieve all ordered topics for a skill, annotated with user completion status.
    """
    topics = db.query(Topic).filter(Topic.skill_id == skill_id).order_by(Topic.order_index.asc()).all()

    completed_topic_ids = set()
    if user_id:
        completed_records = db.query(UserTopicProgress.topic_id).filter(
            UserTopicProgress.user_id == user_id,
            UserTopicProgress.is_completed == True
        ).all()
        completed_topic_ids = {r[0] for r in completed_records}

    result = []
    for t in topics:
        result.append(
            TopicResponse(
                id=t.id,
                skill_id=t.skill_id,
                title=t.title,
                description=t.description,
                order_index=t.order_index,
                is_must_know=t.is_must_know,
                estimated_minutes=t.estimated_minutes,
                is_completed=t.id in completed_topic_ids,
                created_at=t.created_at
            )
        )
    return result


def get_important_topics(
    db: Session, 
    skill_id: int, 
    user_id: Optional[int] = None
) -> List[TopicResponse]:
    """
    Retrieve only the essential Must-Know topics (Section 14) for a skill.
    """
    topics = db.query(Topic).filter(
        Topic.skill_id == skill_id,
        Topic.is_must_know == True
    ).order_by(Topic.order_index.asc()).all()

    completed_topic_ids = set()
    if user_id:
        completed_records = db.query(UserTopicProgress.topic_id).filter(
            UserTopicProgress.user_id == user_id,
            UserTopicProgress.is_completed == True
        ).all()
        completed_topic_ids = {r[0] for r in completed_records}

    result = []
    for t in topics:
        result.append(
            TopicResponse(
                id=t.id,
                skill_id=t.skill_id,
                title=t.title,
                description=t.description,
                order_index=t.order_index,
                is_must_know=True,
                estimated_minutes=t.estimated_minutes,
                is_completed=t.id in completed_topic_ids,
                created_at=t.created_at
            )
        )
    return result


def get_skill_practical(
    db: Session, 
    skill_id: int
) -> List[PracticalContent]:
    """
    Retrieve practical code/syntax examples (technical) or real-world scenarios/case studies (non-technical).
    """
    # Ensure skill exists
    get_skill_by_id_or_slug(db, skill_id)
    return db.query(PracticalContent).filter(
        PracticalContent.skill_id == skill_id
    ).order_by(PracticalContent.order_index.asc()).all()


def toggle_topic_completion(
    db: Session, 
    user_id: int, 
    topic_id: int, 
    is_completed: Optional[bool] = None
) -> UserTopicProgress:
    """
    Toggle or explicitly set topic completion for the authenticated user.
    """
    topic = db.query(Topic).filter(Topic.id == topic_id).first()
    if not topic:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Topic {topic_id} not found."
        )

    progress = db.query(UserTopicProgress).filter(
        UserTopicProgress.user_id == user_id,
        UserTopicProgress.topic_id == topic_id
    ).first()

    now = datetime.now(timezone.utc)
    if not progress:
        target_state = is_completed if is_completed is not None else True
        progress = UserTopicProgress(
            user_id=user_id,
            topic_id=topic_id,
            is_completed=target_state,
            completed_at=now
        )
        db.add(progress)
    else:
        if is_completed is not None:
            progress.is_completed = is_completed
        else:
            progress.is_completed = not progress.is_completed
        progress.completed_at = now

    db.commit()
    db.refresh(progress)
    return progress


def get_user_skill_progress(
    db: Session,
    user_id: int,
    skill_id: int
) -> SkillProgressResponse:
    """
    Compute comprehensive progress metrics and completion requirements for a skill.
    """
    skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if not skill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Skill with ID {skill_id} not found."
        )

    topics = db.query(Topic).filter(Topic.skill_id == skill_id).all()
    total_topics = len(topics)
    topic_ids = [t.id for t in topics]

    must_know_topics = [t for t in topics if t.is_must_know]
    must_know_count = len(must_know_topics)
    must_know_ids = {t.id for t in must_know_topics}

    completed_topic_records = db.query(UserTopicProgress.topic_id).filter(
        UserTopicProgress.user_id == user_id,
        UserTopicProgress.topic_id.in_(topic_ids),
        UserTopicProgress.is_completed == True
    ).all() if topic_ids else []
    
    completed_ids = {r[0] for r in completed_topic_records}
    completed_count = len(completed_ids)
    completed_must_know_count = len(must_know_ids.intersection(completed_ids))

    skill_progress = db.query(UserSkillProgress).filter(
        UserSkillProgress.user_id == user_id,
        UserSkillProgress.skill_id == skill_id
    ).first()

    is_completed = skill_progress.is_completed if skill_progress else False
    completed_at = skill_progress.completed_at if skill_progress else None

    if is_completed:
        progress_percentage = 100
    elif total_topics > 0:
        progress_percentage = round((completed_count / total_topics) * 100)
    else:
        progress_percentage = 0

    if must_know_count > 0:
        can_complete = completed_must_know_count >= must_know_count
    elif total_topics > 0:
        can_complete = completed_count >= (total_topics // 2) or completed_count > 0
    else:
        can_complete = True

    if is_completed:
        completion_requirements = "Skill is marked as completed! You can proceed to Self-Evaluation."
    elif can_complete:
        completion_requirements = f"All {must_know_count} Must-Know topics mastered! Ready to complete skill."
    else:
        remaining = must_know_count - completed_must_know_count
        completion_requirements = f"Master all Must-Know topics ({completed_must_know_count}/{must_know_count} mastered; {remaining} remaining)."

    return SkillProgressResponse(
        skill_id=skill.id,
        skill_name=skill.name,
        skill_category=skill.category,
        is_technical=skill.is_technical,
        total_topics=total_topics,
        completed_topics=completed_count,
        must_know_topics=must_know_count,
        completed_must_know_topics=completed_must_know_count,
        progress_percentage=progress_percentage,
        is_completed=is_completed,
        completed_at=completed_at,
        can_complete=can_complete,
        completion_requirements=completion_requirements
    )


def complete_skill(
    db: Session,
    user_id: int,
    skill_id: int,
    request: Optional[SkillCompletionRequest] = None
) -> SkillProgressResponse:
    """
    Mark a skill as completed in user_skill_progress, enforcing learning flow requirements.
    """
    skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if not skill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Skill with ID {skill_id} not found."
        )

    now = datetime.now(timezone.utc)
    force = request.force if request else False
    complete_all_topics = request.complete_all_topics if request else False

    topics = db.query(Topic).filter(Topic.skill_id == skill_id).all()

    if complete_all_topics:
        for topic in topics:
            record = db.query(UserTopicProgress).filter(
                UserTopicProgress.user_id == user_id,
                UserTopicProgress.topic_id == topic.id
            ).first()
            if not record:
                record = UserTopicProgress(
                    user_id=user_id,
                    topic_id=topic.id,
                    is_completed=True,
                    completed_at=now
                )
                db.add(record)
            else:
                record.is_completed = True
                record.completed_at = now
        db.commit()

    current_progress = get_user_skill_progress(db, user_id, skill_id)

    if not force and not current_progress.can_complete:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot complete skill yet. Learning flow requirement not met: {current_progress.completion_requirements}"
        )

    progress_entry = db.query(UserSkillProgress).filter(
        UserSkillProgress.user_id == user_id,
        UserSkillProgress.skill_id == skill_id
    ).first()

    if not progress_entry:
        progress_entry = UserSkillProgress(
            user_id=user_id,
            skill_id=skill_id,
            status="completed",
            is_completed=True,
            completed_at=now,
            progress_percentage=100
        )
        db.add(progress_entry)
    else:
        progress_entry.status = "completed"
        progress_entry.is_completed = True
        progress_entry.completed_at = now
        progress_entry.progress_percentage = 100

    db.commit()
    db.refresh(progress_entry)
    return get_user_skill_progress(db, user_id, skill_id)


def reset_skill_progress(
    db: Session,
    user_id: int,
    skill_id: int
) -> SkillProgressResponse:
    """
    Reset a user's progress for a skill and its topics.
    """
    skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if not skill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Skill with ID {skill_id} not found."
        )

    progress_entry = db.query(UserSkillProgress).filter(
        UserSkillProgress.user_id == user_id,
        UserSkillProgress.skill_id == skill_id
    ).first()
    if progress_entry:
        progress_entry.status = "in_progress"
        progress_entry.is_completed = False
        progress_entry.completed_at = None
        progress_entry.progress_percentage = 0

    topics = db.query(Topic).filter(Topic.skill_id == skill_id).all()
    for t in topics:
        topic_prog = db.query(UserTopicProgress).filter(
            UserTopicProgress.user_id == user_id,
            UserTopicProgress.topic_id == t.id
        ).first()
        if topic_prog:
            topic_prog.is_completed = False

    db.commit()
    return get_user_skill_progress(db, user_id, skill_id)


def get_overall_goal_progress(
    db: Session,
    user_id: int
) -> Optional[OverallGoalProgressResponse]:
    """
    Retrieve overall milestone progress across the user's active career goal.
    """
    active_selection = db.query(UserGoalSelection).filter(
        UserGoalSelection.user_id == user_id
    ).order_by(UserGoalSelection.selected_at.desc()).first()

    if not active_selection:
        default_goal = db.query(Goal).first()
        if not default_goal:
            return None
        goal = default_goal
    else:
        goal = db.query(Goal).filter(Goal.id == active_selection.goal_id).first() or db.query(Goal).first()

    if not goal:
        return None

    skills = db.query(Skill).filter(Skill.goal_id == goal.id).order_by(Skill.order_index.asc()).all()
    total_skills = len(skills)

    skill_progresses = []
    completed_skills_count = 0

    for s in skills:
        prog = get_user_skill_progress(db, user_id, s.id)
        skill_progresses.append(prog)
        if prog.is_completed:
            completed_skills_count += 1

    overall_percentage = round((completed_skills_count / total_skills) * 100) if total_skills > 0 else 0

    return OverallGoalProgressResponse(
        goal_id=goal.id,
        goal_title=goal.title,
        goal_category=goal.category,
        total_skills=total_skills,
        completed_skills=completed_skills_count,
        overall_percentage=overall_percentage,
        skills=skill_progresses
    )

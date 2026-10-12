from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.user import User
from app.models.goal import Goal
from app.models.skill import Skill
from app.models.topic import Topic
from app.models.user_goal import UserGoalSelection
from app.models.topic_progress import UserTopicProgress
from app.models.skill_progress import UserSkillProgress
from app.models.evaluation import UserSkillEvaluation
from app.models.overall_evaluation import UserGoalEvaluation
from app.models.final_interview import GoalFinalInterviewQuestion, UserInterviewPractice
from app.schemas.dashboard import (
    ComprehensiveDashboardResponse,
    SkillDashboardSummary,
    AchievementBadge,
)
from app.schemas.auth import UserProfileSummaryResponse, UserProfileUpdateRequest, UserResponse


def get_user_dashboard(db: Session, user_id: int) -> ComprehensiveDashboardResponse:
    """
    Compute full unified learning metrics for the user's active career goal,
    including skill completion, topic mastery, estimated hours, evaluation readiness,
    capstone interview prep, and achievement badges (Phase 12).
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found."
        )

    # 1. Active Goal
    active_selection = db.query(UserGoalSelection).filter(
        UserGoalSelection.user_id == user_id
    ).order_by(UserGoalSelection.selected_at.desc()).first()

    if active_selection:
        goal = db.query(Goal).filter(Goal.id == active_selection.goal_id).first()
    else:
        goal = db.query(Goal).first()

    if not goal:
        goal = db.query(Goal).first()

    # 2. Skills & Topics breakdown
    skills = db.query(Skill).filter(Skill.goal_id == goal.id).order_by(Skill.order_index.asc()).all() if goal else []
    total_skills = len(skills)

    skill_summaries: List[SkillDashboardSummary] = []
    completed_skills_count = 0
    in_progress_skills_count = 0

    total_topics_count = 0
    completed_topics_count = 0
    must_know_topics_count = 0
    completed_must_know_count = 0

    estimated_total_minutes = 0
    estimated_completed_minutes = 0

    # User topic progress set
    all_topic_ids = []
    for s in skills:
        all_topic_ids.extend([t.id for t in s.topics])

    completed_topic_ids = set()
    if all_topic_ids:
        c_records = db.query(UserTopicProgress.topic_id).filter(
            UserTopicProgress.user_id == user_id,
            UserTopicProgress.topic_id.in_(all_topic_ids),
            UserTopicProgress.is_completed == True
        ).all()
        completed_topic_ids = {r[0] for r in c_records}

    # User skill progress records
    skill_prog_records = db.query(UserSkillProgress).filter(
        UserSkillProgress.user_id == user_id
    ).all()
    skill_prog_map = {r.skill_id: r for r in skill_prog_records}

    # User skill evaluations
    skill_eval_records = db.query(UserSkillEvaluation).filter(
        UserSkillEvaluation.user_id == user_id
    ).all()
    skill_eval_map = {r.skill_id: r for r in skill_eval_records}

    for s in skills:
        topics = s.topics
        t_total = len(topics)
        total_topics_count += t_total

        t_ids = {t.id for t in topics}
        s_completed_ids = t_ids.intersection(completed_topic_ids)
        t_completed = len(s_completed_ids)
        completed_topics_count += t_completed

        mk_topics = [t for t in topics if t.is_must_know]
        must_know_topics_count += len(mk_topics)
        completed_must_know_count += len({t.id for t in mk_topics}.intersection(completed_topic_ids))

        # Estimated minutes
        for t in topics:
            mins = t.estimated_minutes or 20
            estimated_total_minutes += mins
            if t.id in completed_topic_ids:
                estimated_completed_minutes += mins

        # Skill completion status
        prog = skill_prog_map.get(s.id)
        is_completed = prog.is_completed if prog else False
        completed_at = prog.completed_at if prog else None

        if is_completed:
            completed_skills_count += 1
            progress_pct = 100
        elif t_total > 0:
            progress_pct = round((t_completed / t_total) * 100)
            if t_completed > 0:
                in_progress_skills_count += 1
        else:
            progress_pct = 0

        # Skill evaluation score
        eval_record = skill_eval_map.get(s.id)
        eval_score = eval_record.score if eval_record else None
        eval_pct = eval_record.percentage if eval_record else None

        skill_summaries.append(
            SkillDashboardSummary(
                skill_id=s.id,
                skill_name=s.name,
                skill_slug=s.slug,
                skill_category=s.category,
                order_index=s.order_index,
                is_technical=s.is_technical,
                total_topics=t_total,
                completed_topics=t_completed,
                progress_percentage=progress_pct,
                is_completed=is_completed,
                completed_at=completed_at,
                evaluation_score=eval_score,
                evaluation_percentage=eval_pct
            )
        )

    overall_skill_pct = round((completed_skills_count / total_skills) * 100) if total_skills > 0 else 0
    overall_topic_pct = round((completed_topics_count / total_topics_count) * 100) if total_topics_count > 0 else 0
    estimated_completed_hours = round(estimated_completed_minutes / 60.0, 1)

    # 3. Overall Goal Evaluation
    latest_goal_eval = None
    if goal:
        latest_goal_eval = db.query(UserGoalEvaluation).filter(
            UserGoalEvaluation.user_id == user_id,
            UserGoalEvaluation.goal_id == goal.id
        ).order_by(UserGoalEvaluation.completed_at.desc()).first()

    has_overall_eval = latest_goal_eval is not None
    overall_eval_score = latest_goal_eval.score if latest_goal_eval else None
    overall_eval_pct = latest_goal_eval.percentage if latest_goal_eval else None
    overall_readiness_level = latest_goal_eval.readiness_level if latest_goal_eval else None

    # 4. Final Capstone Interview metrics (Section 21-23)
    total_fiq = 15
    practiced_fiq_count = 0
    if goal:
        fiq_ids = [q.id for q in db.query(GoalFinalInterviewQuestion.id).filter_by(goal_id=goal.id).all()]
        total_fiq = len(fiq_ids) if len(fiq_ids) > 0 else 15
        if fiq_ids:
            practiced_fiq_count = db.query(UserInterviewPractice).filter(
                UserInterviewPractice.user_id == user_id,
                UserInterviewPractice.question_id.in_(fiq_ids),
                UserInterviewPractice.is_practiced == True
            ).count()

    interview_progress_pct = round((practiced_fiq_count / total_fiq) * 100) if total_fiq > 0 else 0

    # 5. Milestone Badges / Achievements
    achievements: List[AchievementBadge] = [
        AchievementBadge(
            id="enrolled_goal",
            title="Goal Chosen",
            description="Selected an ambitious career trajectory to pursue.",
            icon="Target",
            is_unlocked=goal is not None,
            category="Milestone"
        ),
        AchievementBadge(
            id="first_topic",
            title="First Step",
            description="Mastered your first learning topic in the curriculum.",
            icon="Sparkles",
            is_unlocked=completed_topics_count >= 1,
            category="Learning"
        ),
        AchievementBadge(
            id="topic_pioneer",
            title="Topic Pioneer",
            description="Completed at least 5 curriculum topics with dedication.",
            icon="BookOpen",
            is_unlocked=completed_topics_count >= 5,
            category="Learning"
        ),
        AchievementBadge(
            id="first_skill",
            title="Skill Finisher",
            description="Achieved full mastery of your first individual skill.",
            icon="CheckCircle2",
            is_unlocked=completed_skills_count >= 1,
            category="Milestone"
        ),
        AchievementBadge(
            id="halfway_milestone",
            title="Halfway Hero",
            description="Mastered at least 50% of the skills in your career track.",
            icon="Layers",
            is_unlocked=total_skills > 0 and completed_skills_count >= (total_skills / 2),
            category="Milestone"
        ),
        AchievementBadge(
            id="goal_master",
            title="Goal Curriculum Master",
            description="Completed 100% of all required skills in your career goal.",
            icon="Award",
            is_unlocked=total_skills > 0 and completed_skills_count == total_skills,
            category="Milestone"
        ),
        AchievementBadge(
            id="evaluator",
            title="Diagnostic Master",
            description="Completed skill diagnostic self-evaluations or overall evaluation.",
            icon="FileCheck",
            is_unlocked=len(skill_eval_records) > 0 or has_overall_eval,
            category="Evaluation"
        ),
        AchievementBadge(
            id="interview_ready",
            title="Interview Capstone Ready",
            description="Practiced at least 5 must-know capstone interview questions.",
            icon="Trophy",
            is_unlocked=practiced_fiq_count >= 5,
            category="Interview"
        ),
    ]

    return ComprehensiveDashboardResponse(
        user_id=user.id,
        user_name=user.name,
        user_email=user.email,
        member_since=user.created_at,
        goal_id=goal.id if goal else None,
        goal_title=goal.title if goal else None,
        goal_slug=goal.slug if goal else None,
        goal_category=goal.category if goal else None,
        goal_description=goal.description if goal else None,
        total_skills=total_skills,
        completed_skills=completed_skills_count,
        in_progress_skills=in_progress_skills_count,
        overall_skill_percentage=overall_skill_pct,
        total_topics=total_topics_count,
        completed_topics=completed_topics_count,
        must_know_topics=must_know_topics_count,
        completed_must_know_topics=completed_must_know_count,
        topic_percentage=overall_topic_pct,
        estimated_total_minutes=estimated_total_minutes,
        estimated_completed_minutes=estimated_completed_minutes,
        estimated_completed_hours=estimated_completed_hours,
        completed_skill_evaluations=len(skill_eval_records),
        has_overall_evaluation=has_overall_eval,
        overall_eval_score=overall_eval_score,
        overall_eval_percentage=overall_eval_pct,
        overall_readiness_level=overall_readiness_level,
        total_interview_questions=total_fiq,
        practiced_interview_questions=practiced_fiq_count,
        interview_progress_percentage=interview_progress_pct,
        achievements=achievements,
        skills=skill_summaries
    )


def get_user_profile_summary(db: Session, user_id: int) -> UserProfileSummaryResponse:
    """
    Retrieve compact user profile summary for the Profile page.
    """
    dash = get_user_dashboard(db, user_id)
    user = db.query(User).filter(User.id == user_id).first()

    unlocked_achievements = sum(1 for a in dash.achievements if a.is_unlocked)

    return UserProfileSummaryResponse(
        user=UserResponse.model_validate(user),
        active_goal_id=dash.goal_id,
        active_goal_title=dash.goal_title,
        active_goal_slug=dash.goal_slug,
        active_goal_category=dash.goal_category,
        skills_completed=dash.completed_skills,
        total_skills=dash.total_skills,
        skill_completion_percentage=dash.overall_skill_percentage,
        topics_completed=dash.completed_topics,
        total_topics=dash.total_topics,
        readiness_level=dash.overall_readiness_level,
        interview_practiced_count=dash.practiced_interview_questions,
        achievements_count=unlocked_achievements,
        total_achievements=len(dash.achievements)
    )


def update_user_profile(
    db: Session,
    user_id: int,
    request: UserProfileUpdateRequest
) -> UserResponse:
    """
    Update basic user profile details (such as display name).
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found."
        )

    if request.name and request.name.strip():
        user.name = request.name.strip()

    db.commit()
    db.refresh(user)
    return UserResponse.model_validate(user)

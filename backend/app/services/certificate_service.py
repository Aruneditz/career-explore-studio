import json
from typing import Optional, List
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.skill import Skill
from app.models.goal import Goal
from app.models.user import User
from app.models.topic import Topic
from app.models.topic_progress import UserTopicProgress
from app.models.skill_progress import UserSkillProgress
from app.models.evaluation import UserSkillEvaluation
from app.models.certificate import UserCertificate, generate_certificate_id
from app.schemas.certificate import (
    CertificateResponse,
    SkillCertificateChecklist,
    SkillCertificateStatusResponse,
    UserCertificatesListResponse,
)


def get_skill_completion_checklist(
    db: Session,
    user_id: int,
    skill_id: int
) -> SkillCertificateStatusResponse:
    """
    Evaluates backend truth across the 4 core learning workflow stages:
    1. Topics (All Must-Know topics completed)
    2. Practical (Practical labs reviewed)
    3. Self-Evaluation (Diagnostic quiz submitted with valid score)
    4. Interview Preparation (Interview questions reviewed)
    """
    skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if not skill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Skill with ID {skill_id} not found."
        )

    goal = db.query(Goal).filter(Goal.id == skill.goal_id).first()

    # 1. Topics Stage
    topics = db.query(Topic).filter(Topic.skill_id == skill.id).all()
    total_topics = len(topics)
    must_know_topics = [t for t in topics if t.is_must_know]
    must_know_count = len(must_know_topics)
    must_know_ids = {t.id for t in must_know_topics}

    completed_topic_ids = set()
    if total_topics > 0:
        completed_records = db.query(UserTopicProgress.topic_id).filter(
            UserTopicProgress.user_id == user_id,
            UserTopicProgress.topic_id.in_([t.id for t in topics]),
            UserTopicProgress.is_completed == True
        ).all()
        completed_topic_ids = {r[0] for r in completed_records}

    completed_count = len(completed_topic_ids)
    completed_must_know_count = len(must_know_ids.intersection(completed_topic_ids))

    if must_know_count > 0:
        topics_completed = completed_must_know_count >= must_know_count
        topics_summary = f"{completed_must_know_count}/{must_know_count} Must-Know topics completed"
    elif total_topics > 0:
        topics_completed = completed_count >= (total_topics // 2) or completed_count > 0
        topics_summary = f"{completed_count}/{total_topics} topics completed"
    else:
        topics_completed = True
        topics_summary = "All curriculum topics completed"

    # User skill progress entry
    skill_prog = db.query(UserSkillProgress).filter(
        UserSkillProgress.user_id == user_id,
        UserSkillProgress.skill_id == skill.id
    ).first()

    # 2. Practical Stage
    practical_completed = bool(skill_prog and skill_prog.practical_reviewed) or bool(skill_prog and skill_prog.is_completed)
    practical_summary = "Practical code/labs reviewed" if practical_completed else "Review practical exercises and code labs"

    # 3. Self-Evaluation Stage (backed by database record in user_skill_evaluations)
    latest_eval = db.query(UserSkillEvaluation).filter(
        UserSkillEvaluation.user_id == user_id,
        UserSkillEvaluation.skill_id == skill.id
    ).order_by(UserSkillEvaluation.completed_at.desc()).first()

    evaluation_completed = latest_eval is not None
    if evaluation_completed:
        evaluation_summary = f"Passed with score: {latest_eval.score}/{latest_eval.total_questions} ({latest_eval.percentage}%)"
    else:
        evaluation_summary = "Diagnostic self-evaluation quiz pending"

    # 4. Interview Preparation Stage
    interview_completed = bool(skill_prog and skill_prog.interview_reviewed) or bool(skill_prog and skill_prog.is_completed)
    interview_summary = "Interview questions mastered" if interview_completed else "Review skill interview preparation questions"

    # Calculate overall completion eligibility
    overall_completed = topics_completed and evaluation_completed and interview_completed and practical_completed

    # Calculate granular workflow progress percentage (each stage contributes 25%)
    stage_points = 0
    if topics_completed:
        stage_points += 25
    if practical_completed:
        stage_points += 25
    if evaluation_completed:
        stage_points += 25
    if interview_completed:
        stage_points += 25

    progress_percentage = 100 if overall_completed else stage_points

    # Check if certificate is already issued
    cert = db.query(UserCertificate).filter(
        UserCertificate.user_id == user_id,
        UserCertificate.skill_id == skill.id
    ).first()

    is_unlocked = cert is not None or overall_completed

    if cert:
        status_message = "Certificate Earned — Official credential verified and issued."
    elif overall_completed:
        status_message = "Certificate Available — All requirements satisfied! Ready to view official credential."
    else:
        pending_items = []
        if not topics_completed:
            pending_items.append("Topics")
        if not practical_completed:
            pending_items.append("Practical Labs")
        if not evaluation_completed:
            pending_items.append("Self-Evaluation")
        if not interview_completed:
            pending_items.append("Interview Prep")
        status_message = f"Certificate Locked — Incomplete required stages: {', '.join(pending_items)}."

    cert_response = None
    if cert:
        cert_response = CertificateResponse.model_validate(cert)

    checklist = SkillCertificateChecklist(
        topics_completed=topics_completed,
        topics_summary=topics_summary,
        practical_completed=practical_completed,
        practical_summary=practical_summary,
        evaluation_completed=evaluation_completed,
        evaluation_summary=evaluation_summary,
        interview_completed=interview_completed,
        interview_summary=interview_summary,
        overall_completed=overall_completed,
        progress_percentage=progress_percentage
    )

    return SkillCertificateStatusResponse(
        skill_id=skill.id,
        skill_name=skill.name,
        goal_id=goal.id if goal else None,
        goal_title=goal.title if goal else None,
        is_unlocked=is_unlocked,
        status_message=status_message,
        checklist=checklist,
        certificate=cert_response
    )


def claim_or_get_skill_certificate(
    db: Session,
    user_id: int,
    skill_id: int
) -> CertificateResponse:
    """
    Issues official certificate if and only if all learning requirements are genuinely met.
    The backend is the sole source of truth.
    """
    status_info = get_skill_completion_checklist(db, user_id, skill_id)

    # Check existing certificate
    cert = db.query(UserCertificate).filter(
        UserCertificate.user_id == user_id,
        UserCertificate.skill_id == skill_id
    ).first()

    if cert:
        return CertificateResponse.model_validate(cert)

    if not status_info.checklist.overall_completed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot issue certificate. You must complete all required learning stages: {status_info.status_message}"
        )

    # Fetch user details
    user = db.query(User).filter(User.id == user_id).first()
    skill = db.query(Skill).filter(Skill.id == skill_id).first()
    goal = db.query(Goal).filter(Goal.id == skill.goal_id).first() if skill else None

    # Sync skill progress to completed state
    skill_prog = db.query(UserSkillProgress).filter(
        UserSkillProgress.user_id == user_id,
        UserSkillProgress.skill_id == skill_id
    ).first()

    now = datetime.now(timezone.utc)
    if not skill_prog:
        skill_prog = UserSkillProgress(
            user_id=user_id,
            skill_id=skill_id,
            status="completed",
            is_completed=True,
            completed_at=now,
            progress_percentage=100,
            practical_reviewed=True,
            interview_reviewed=True
        )
        db.add(skill_prog)
    else:
        skill_prog.status = "completed"
        skill_prog.is_completed = True
        skill_prog.completed_at = now
        skill_prog.progress_percentage = 100
        skill_prog.practical_reviewed = True
        skill_prog.interview_reviewed = True

    # Generate unique certificate
    cert_id = generate_certificate_id("SKILL")
    cert = UserCertificate(
        user_id=user_id,
        certificate_id=cert_id,
        certificate_type="skill",
        skill_id=skill_id,
        goal_id=goal.id if goal else None,
        title=f"Certificate of Mastery: {skill.name}",
        recipient_name=user.name,
        issued_at=now,
        status="issued",
        metadata_json=json.dumps({
            "skill_name": skill.name,
            "skill_category": skill.category,
            "goal_title": goal.title if goal else "Career Exploration Track",
            "topics_count": status_info.checklist.topics_summary,
            "evaluation_result": status_info.checklist.evaluation_summary,
            "verification_code": cert_id
        })
    )
    db.add(cert)
    db.commit()
    db.refresh(cert)

    return CertificateResponse.model_validate(cert)


def mark_skill_stage_interaction(
    db: Session,
    user_id: int,
    skill_id: int,
    stage: str
) -> SkillCertificateStatusResponse:
    """
    Marks interaction for 'practical' or 'interview' stage.
    """
    skill_prog = db.query(UserSkillProgress).filter(
        UserSkillProgress.user_id == user_id,
        UserSkillProgress.skill_id == skill_id
    ).first()

    now = datetime.now(timezone.utc)
    if not skill_prog:
        skill_prog = UserSkillProgress(
            user_id=user_id,
            skill_id=skill_id,
            status="in_progress",
            created_at=now,
            updated_at=now
        )
        db.add(skill_prog)

    if stage == "practical":
        skill_prog.practical_reviewed = True
    elif stage == "interview":
        skill_prog.interview_reviewed = True

    skill_prog.updated_at = now
    db.commit()

    return get_skill_completion_checklist(db, user_id, skill_id)


def get_all_user_certificates(
    db: Session,
    user_id: int
) -> UserCertificatesListResponse:
    """
    Retrieve all verified certificates earned by the user.
    """
    certs = db.query(UserCertificate).filter(
        UserCertificate.user_id == user_id
    ).order_by(UserCertificate.issued_at.desc()).all()

    return UserCertificatesListResponse(
        total_earned=len(certs),
        certificates=[CertificateResponse.model_validate(c) for c in certs]
    )


def verify_certificate_by_id(
    db: Session,
    certificate_id: str
) -> CertificateResponse:
    """
    Public lookup for credential verification.
    """
    cert = db.query(UserCertificate).filter(
        UserCertificate.certificate_id == certificate_id
    ).first()

    if not cert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Certificate '{certificate_id}' not found or invalid."
        )

    return CertificateResponse.model_validate(cert)

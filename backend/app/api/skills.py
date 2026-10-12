from typing import List, Optional
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.api.deps import get_current_user, get_optional_current_user
from app.models.user import User
from app.models.evaluation import UserSkillEvaluation
from app.schemas.skill import SkillOverviewResponse, SkillDetailResponse
from app.schemas.topic import TopicResponse, TopicToggleRequest, TopicToggleResponse
from app.schemas.practical import PracticalContentResponse
from app.schemas.skill_progress import SkillProgressResponse, SkillCompletionRequest
from app.schemas.evaluation import (
    EvaluationQuestionResponse,
    EvaluationSubmissionRequest,
    EvaluationResultResponse,
)
from app.schemas.skill_interview import (
    SkillInterviewQuestionResponse,
    SkillSequenceInfoResponse,
)
from app.services import skill_service, evaluation_service, skill_interview_service

router = APIRouter()


@router.get("/{identifier}", response_model=SkillOverviewResponse)
def get_skill_overview(
    identifier: str,
    current_user: Optional[User] = Depends(get_optional_current_user),
    db: Session = Depends(get_db)
):
    """
    Get detailed overview information for a skill (Section 12),
    including completion stats if authenticated.
    """
    user_id = current_user.id if current_user else None
    return skill_service.get_skill_by_id_or_slug(db, identifier, user_id=user_id)


@router.get("/{skill_id}/topics", response_model=List[TopicResponse])
def get_complete_topics(
    skill_id: int,
    current_user: Optional[User] = Depends(get_optional_current_user),
    db: Session = Depends(get_db)
):
    """
    Get complete topic list for a skill (Section 13),
    annotated with is_completed for the authenticated user.
    """
    user_id = current_user.id if current_user else None
    return skill_service.get_skill_topics(db, skill_id, user_id=user_id)


@router.get("/{skill_id}/important-topics", response_model=List[TopicResponse])
def get_important_topics(
    skill_id: int,
    current_user: Optional[User] = Depends(get_optional_current_user),
    db: Session = Depends(get_db)
):
    """
    Get only essential Must-Know topics for a skill (Section 14),
    annotated with is_completed for the authenticated user.
    """
    user_id = current_user.id if current_user else None
    return skill_service.get_important_topics(db, skill_id, user_id=user_id)


@router.get("/{skill_id}/practical", response_model=List[PracticalContentResponse])
def get_practical_content(
    skill_id: int,
    db: Session = Depends(get_db)
):
    """
    Get practical exercises, code syntax, scenarios, or case studies (Section 15).
    Works for both technical and non-technical skills.
    """
    return skill_service.get_skill_practical(db, skill_id)


@router.post("/{skill_id}/topics/{topic_id}/toggle", response_model=TopicToggleResponse)
def toggle_topic_progress(
    skill_id: int,
    topic_id: int,
    request: Optional[TopicToggleRequest] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Mark a topic as completed or uncompleted for the current user.
    Protected endpoint.
    """
    explicit_state = request.is_completed if request else None
    progress = skill_service.toggle_topic_completion(
        db, 
        user_id=current_user.id, 
        topic_id=topic_id, 
        is_completed=explicit_state
    )
    return TopicToggleResponse(
        topic_id=progress.topic_id,
        is_completed=progress.is_completed,
        completed_at=progress.completed_at
    )


@router.get("/{skill_id}/progress", response_model=SkillProgressResponse)
def get_skill_progress(
    skill_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get current user's progress and completion status for a specific skill (Section 16).
    Protected endpoint.
    """
    return skill_service.get_user_skill_progress(db, user_id=current_user.id, skill_id=skill_id)


@router.post("/{skill_id}/complete", response_model=SkillProgressResponse)
def complete_skill_endpoint(
    skill_id: int,
    request: Optional[SkillCompletionRequest] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Mark a skill as completed for the authenticated user (Section 16).
    Verifies learning flow requirements unless forced.
    Protected endpoint.
    """
    return skill_service.complete_skill(
        db,
        user_id=current_user.id,
        skill_id=skill_id,
        request=request
    )


@router.post("/{skill_id}/reset-progress", response_model=SkillProgressResponse)
def reset_skill_progress_endpoint(
    skill_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return skill_service.reset_skill_progress(db, user_id=current_user.id, skill_id=skill_id)


@router.get("/{skill_id}/evaluation/questions", response_model=List[EvaluationQuestionResponse])
def get_evaluation_questions_endpoint(
    skill_id: int,
    db: Session = Depends(get_db)
):
    """
    Get personal self-evaluation questions for a skill (Section 17).
    """
    return evaluation_service.get_skill_evaluation_questions(db, skill_id=skill_id)


@router.get("/{skill_id}/evaluation/latest", response_model=Optional[EvaluationResultResponse])
def get_latest_evaluation_endpoint(
    skill_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get current user's latest completed self-evaluation results and feedback (Section 17).
    Protected endpoint.
    """
    return evaluation_service.get_latest_user_evaluation(db, user_id=current_user.id, skill_id=skill_id)


@router.post("/{skill_id}/evaluation/submit", response_model=EvaluationResultResponse)
def submit_evaluation_endpoint(
    skill_id: int,
    request: EvaluationSubmissionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Submit evaluation answers, calculate score, evaluate strong/weak areas, and persist (Section 17).
    Protected endpoint.
    """
    return evaluation_service.submit_skill_evaluation(
        db,
        user_id=current_user.id,
        skill_id=skill_id,
        request=request
    )


@router.get("/evaluation/records/{evaluation_id}", response_model=EvaluationResultResponse)
def get_evaluation_record_by_id(
    evaluation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retrieve a specific evaluation result by database ID.
    Strictly verifies user ownership and blocks unauthorized cross-user access.
    """
    eval_record = db.query(UserSkillEvaluation).filter(UserSkillEvaluation.id == evaluation_id).first()
    if not eval_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Evaluation with ID {evaluation_id} not found."
        )
    if eval_record.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden: You do not have permission to access another user's evaluation report."
        )
    return evaluation_service.get_latest_user_evaluation(db, user_id=current_user.id, skill_id=eval_record.skill_id)


@router.get("/{skill_id}/interview-questions", response_model=List[SkillInterviewQuestionResponse])
def get_interview_questions_endpoint(
    skill_id: int,
    difficulty: Optional[str] = Query(None, description="Optional difficulty filter: Basic, Intermediate, Advanced"),
    db: Session = Depends(get_db)
):
    """
    Get skill-level interview preparation questions (Section 18).
    Supports difficulty filtering (Basic, Intermediate, Advanced).
    """
    return skill_interview_service.get_skill_interview_questions(
        db,
        skill_id=skill_id,
        difficulty=difficulty
    )


@router.get("/{skill_id}/sequence", response_model=SkillSequenceInfoResponse)
def get_skill_sequence_endpoint(
    skill_id: int,
    db: Session = Depends(get_db)
):
    """
    Get progression details for the skill within its career goal sequence (Section 19).
    Identifies the next skill or signals readiness for capstone overall evaluation.
    """
    return skill_interview_service.get_skill_sequence_progression(db, skill_id=skill_id)


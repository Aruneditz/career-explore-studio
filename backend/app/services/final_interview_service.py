from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.goal import Goal
from app.models.final_interview import (
    GoalFinalInterviewQuestion,
    UserInterviewPractice,
)
from app.schemas.final_interview import (
    FinalInterviewQuestionResponse,
    FinalInterviewPracticeToggleRequest,
    FinalInterviewPracticeStatusResponse,
    FinalInterviewHubResponse,
)


def get_final_interview_hub(
    db: Session,
    goal_id: int,
    user_id: Optional[int] = None
) -> FinalInterviewHubResponse:
    """
    Retrieve the capstone interview preparation hub for a goal,
    including the EXACTLY 15 MUST-KNOW INTERVIEW QUESTIONS (Section 22)
    and the user's practice progress (Section 23).
    """
    goal = db.query(Goal).filter(Goal.id == goal_id).first()
    if not goal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Career goal with ID {goal_id} not found."
        )

    questions = db.query(GoalFinalInterviewQuestion).filter(
        GoalFinalInterviewQuestion.goal_id == goal_id
    ).order_by(GoalFinalInterviewQuestion.question_number.asc()).all()

    practiced_map = {}
    if user_id:
        practice_records = db.query(UserInterviewPractice).filter(
            UserInterviewPractice.user_id == user_id,
            UserInterviewPractice.is_practiced == True
        ).all()
        practiced_map = {r.question_id: r.practiced_at for r in practice_records}

    question_responses: List[FinalInterviewQuestionResponse] = []
    for q in questions:
        is_p = q.id in practiced_map
        question_responses.append(
            FinalInterviewQuestionResponse(
                id=q.id,
                goal_id=q.goal_id,
                question_number=q.question_number,
                question=q.question,
                category=q.category,
                why_asked=q.why_asked,
                interviewer_looking_for=q.interviewer_looking_for,
                detailed_answer=q.detailed_answer,
                code_or_practical_example=q.code_or_practical_example,
                scenario_example=q.scenario_example,
                response_structure_star=q.response_structure_star,
                what_not_to_say=q.what_not_to_say,
                is_practiced=is_p,
                practiced_at=practiced_map.get(q.id)
            )
        )

    total_q = len(questions)
    active_q_ids = {q.id for q in questions}
    practiced_count = len(set(practiced_map.keys()).intersection(active_q_ids))
    progress_percentage = round((practiced_count / total_q) * 100) if total_q > 0 else 0

    categories = [
        "Core Fundamentals",
        "Practical & Scenario-Based",
        "Advanced & Problem Solving"
    ]

    return FinalInterviewHubResponse(
        goal_id=goal.id,
        goal_title=goal.title,
        total_questions=total_q,
        practiced_count=practiced_count,
        progress_percentage=progress_percentage,
        practiced_percentage=float(progress_percentage),
        categories=categories,
        questions=question_responses
    )


def toggle_question_practice(
    db: Session,
    user_id: int,
    request: FinalInterviewPracticeToggleRequest
) -> FinalInterviewQuestionResponse:
    """
    Toggle or explicitly set the 'Practiced / Understood' status of a final interview question (Section 23).
    """
    question = db.query(GoalFinalInterviewQuestion).filter(
        GoalFinalInterviewQuestion.id == request.question_id
    ).first()
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Interview question with ID {request.question_id} not found."
        )

    record = db.query(UserInterviewPractice).filter(
        UserInterviewPractice.user_id == user_id,
        UserInterviewPractice.question_id == request.question_id
    ).first()

    now = datetime.now(timezone.utc)
    if record:
        if request.is_practiced is not None:
            record.is_practiced = request.is_practiced
        else:
            record.is_practiced = not record.is_practiced
        record.practiced_at = now
    else:
        new_status = request.is_practiced if request.is_practiced is not None else True
        record = UserInterviewPractice(
            user_id=user_id,
            question_id=request.question_id,
            is_practiced=new_status,
            practiced_at=now
        )
        db.add(record)

    db.commit()
    db.refresh(record)

    return FinalInterviewQuestionResponse(
        id=question.id,
        goal_id=question.goal_id,
        question_number=question.question_number,
        question=question.question,
        category=question.category,
        why_asked=question.why_asked,
        interviewer_looking_for=question.interviewer_looking_for,
        detailed_answer=question.detailed_answer,
        code_or_practical_example=question.code_or_practical_example,
        scenario_example=question.scenario_example,
        response_structure_star=question.response_structure_star,
        what_not_to_say=question.what_not_to_say,
        is_practiced=record.is_practiced,
        practiced_at=record.practiced_at if record.is_practiced else None
    )


def get_practice_status(
    db: Session,
    user_id: int,
    goal_id: int
) -> FinalInterviewPracticeStatusResponse:
    """
    Retrieve user's practiced question metrics and IDs for a goal.
    """
    goal = db.query(Goal).filter(Goal.id == goal_id).first()
    if not goal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Career goal with ID {goal_id} not found."
        )

    questions = db.query(GoalFinalInterviewQuestion).filter(
        GoalFinalInterviewQuestion.goal_id == goal_id
    ).all()
    q_ids = {q.id for q in questions}

    practice_records = db.query(UserInterviewPractice).filter(
        UserInterviewPractice.user_id == user_id,
        UserInterviewPractice.question_id.in_(q_ids),
        UserInterviewPractice.is_practiced == True
    ).all()

    practiced_ids = [r.question_id for r in practice_records]
    total_q = len(questions)
    count = len(practiced_ids)
    pct = round((count / total_q) * 100) if total_q > 0 else 0

    return FinalInterviewPracticeStatusResponse(
        goal_id=goal.id,
        goal_title=goal.title,
        total_questions=total_q,
        practiced_questions=count,
        practiced_count=count,
        progress_percentage=pct,
        practiced_question_ids=practiced_ids
    )

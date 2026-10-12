import json
from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.skill import Skill
from app.models.evaluation import EvaluationQuestion, UserSkillEvaluation
from app.schemas.evaluation import (
    EvaluationOption,
    EvaluationQuestionResponse,
    EvaluationSubmissionRequest,
    QuestionResult,
    EvaluationResultResponse,
)


def get_skill_evaluation_questions(
    db: Session,
    skill_id: int
) -> List[EvaluationQuestionResponse]:
    """
    Retrieve evaluation questions for a skill without revealing correct answers.
    """
    skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if not skill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Skill with ID {skill_id} not found."
        )

    questions = db.query(EvaluationQuestion).filter(
        EvaluationQuestion.skill_id == skill_id
    ).order_by(EvaluationQuestion.order_index.asc()).all()

    results = []
    for q in questions:
        try:
            raw_options = json.loads(q.options_json)
            options = [EvaluationOption(id=opt["id"], text=opt["text"]) for opt in raw_options]
        except Exception:
            options = []

        results.append(
            EvaluationQuestionResponse(
                id=q.id,
                skill_id=q.skill_id,
                question_text=q.question_text,
                question_type=q.question_type,
                options=options,
                topic_area=q.topic_area,
                order_index=q.order_index
            )
        )
    return results


def submit_skill_evaluation(
    db: Session,
    user_id: int,
    skill_id: int,
    request: EvaluationSubmissionRequest
) -> EvaluationResultResponse:
    """
    Grade user answers, categorize strong vs weak topic areas, generate tailored improvement feedback,
    and persist results in the database.
    """
    skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if not skill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Skill with ID {skill_id} not found."
        )

    questions = db.query(EvaluationQuestion).filter(
        EvaluationQuestion.skill_id == skill_id
    ).order_by(EvaluationQuestion.order_index.asc()).all()

    if not questions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No evaluation questions configured for skill ID {skill_id}."
        )

    total_questions = len(questions)
    score = 0
    strong_areas_set = set()
    weak_areas_set = set()
    question_breakdown: List[QuestionResult] = []

    for q in questions:
        selected_option = request.answers.get(str(q.id)) or request.answers.get(q.id)
        is_correct = (selected_option == q.correct_option) if selected_option else False

        if is_correct:
            score += 1
            if q.topic_area:
                strong_areas_set.add(q.topic_area)
        else:
            if q.topic_area:
                weak_areas_set.add(q.topic_area)

        question_breakdown.append(
            QuestionResult(
                question_id=q.id,
                question_text=q.question_text,
                selected_option=selected_option,
                correct_option=q.correct_option,
                is_correct=is_correct,
                explanation=q.explanation,
                topic_area=q.topic_area
            )
        )

    # Disallow an area from being both strong and weak; weak takes precedence for learning
    strong_areas = sorted(list(strong_areas_set - weak_areas_set))
    weak_areas = sorted(list(weak_areas_set))

    percentage = round((score / total_questions) * 100)

    # Performance Level
    if percentage >= 80:
        performance_level = "Mastery"
        feedback_summary = (
            f"Outstanding performance! You scored {score}/{total_questions} ({percentage}%), demonstrating strong "
            f"conceptual command and practical problem-solving capability in {skill.name}."
        )
    elif percentage >= 60:
        performance_level = "Proficient"
        feedback_summary = (
            f"Good progress! You scored {score}/{total_questions} ({percentage}%), showing solid baseline comprehension "
            f"in {skill.name}, with room to refine precision in nuanced edge cases."
        )
    else:
        performance_level = "Developing"
        feedback_summary = (
            f"Foundational review recommended. You scored {score}/{total_questions} ({percentage}%). "
            f"Revisiting key Must-Know concepts in {skill.name} will significantly improve your confidence."
        )

    # Actionable Improvement Suggestions
    suggestions: List[str] = []
    if weak_areas:
        for area in weak_areas[:3]:
            suggestions.append(f"Review core principles and practical exercises specifically around '{area}'.")
    else:
        suggestions.append(f"Maintain your strong edge in {skill.name} by preparing for advanced technical interview questions.")

    if percentage < 80:
        suggestions.append("Revisit the Must-Know Topics and Practical Section before advancing to technical interviews.")
    else:
        suggestions.append("You are ready for stage-specific interview practice! Proceed to the Interview Preparation section.")

    now = datetime.now(timezone.utc)

    # Persist in user_skill_evaluations
    evaluation_record = UserSkillEvaluation(
        user_id=user_id,
        skill_id=skill_id,
        score=score,
        total_questions=total_questions,
        percentage=percentage,
        answers_json=json.dumps(request.answers),
        strong_areas_json=json.dumps(strong_areas),
        weak_areas_json=json.dumps(weak_areas),
        feedback_summary=feedback_summary,
        improvement_suggestions_json=json.dumps(suggestions),
        completed_at=now
    )
    db.add(evaluation_record)
    db.commit()
    db.refresh(evaluation_record)

    return EvaluationResultResponse(
        id=evaluation_record.id,
        skill_id=skill.id,
        score=score,
        total_questions=total_questions,
        percentage=percentage,
        performance_level=performance_level,
        strong_areas=strong_areas,
        weak_areas=weak_areas,
        feedback_summary=feedback_summary,
        improvement_suggestions=suggestions,
        question_breakdown=question_breakdown,
        completed_at=evaluation_record.completed_at
    )


def get_latest_user_evaluation(
    db: Session,
    user_id: int,
    skill_id: int
) -> Optional[EvaluationResultResponse]:
    """
    Retrieve the user's most recent evaluation attempt for this skill.
    """
    skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if not skill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Skill with ID {skill_id} not found."
        )

    latest = db.query(UserSkillEvaluation).filter(
        UserSkillEvaluation.user_id == user_id,
        UserSkillEvaluation.skill_id == skill_id
    ).order_by(UserSkillEvaluation.completed_at.desc()).first()

    if not latest:
        return None

    # Reconstruct question breakdown
    questions = db.query(EvaluationQuestion).filter(
        EvaluationQuestion.skill_id == skill_id
    ).order_by(EvaluationQuestion.order_index.asc()).all()

    try:
        user_answers = json.loads(latest.answers_json)
    except Exception:
        user_answers = {}

    question_breakdown: List[QuestionResult] = []
    for q in questions:
        selected_option = user_answers.get(str(q.id)) or user_answers.get(q.id)
        is_correct = (selected_option == q.correct_option) if selected_option else False
        question_breakdown.append(
            QuestionResult(
                question_id=q.id,
                question_text=q.question_text,
                selected_option=selected_option,
                correct_option=q.correct_option,
                is_correct=is_correct,
                explanation=q.explanation,
                topic_area=q.topic_area
            )
        )

    try:
        strong_areas = json.loads(latest.strong_areas_json)
    except Exception:
        strong_areas = []

    try:
        weak_areas = json.loads(latest.weak_areas_json)
    except Exception:
        weak_areas = []

    try:
        suggestions = json.loads(latest.improvement_suggestions_json)
    except Exception:
        suggestions = []

    if latest.percentage >= 80:
        performance_level = "Mastery"
    elif latest.percentage >= 60:
        performance_level = "Proficient"
    else:
        performance_level = "Developing"

    return EvaluationResultResponse(
        id=latest.id,
        skill_id=skill.id,
        score=latest.score,
        total_questions=latest.total_questions,
        percentage=latest.percentage,
        performance_level=performance_level,
        strong_areas=strong_areas,
        weak_areas=weak_areas,
        feedback_summary=latest.feedback_summary,
        improvement_suggestions=suggestions,
        question_breakdown=question_breakdown,
        completed_at=latest.completed_at
    )

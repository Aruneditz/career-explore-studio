import json
from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.goal import Goal
from app.models.overall_evaluation import (
    OverallGoalEvaluationQuestion,
    UserGoalEvaluation,
)
from app.schemas.overall_evaluation import (
    OverallQuestionOption,
    OverallQuestionResponse,
    OverallEvaluationSubmissionRequest,
    OverallQuestionResult,
    OverallEvaluationResultResponse,
)


def get_goal_overall_questions(
    db: Session,
    goal_id: int
) -> List[OverallQuestionResponse]:
    """
    Retrieve cross-skill evaluation questions for a career goal without leaking correct answers.
    """
    goal = db.query(Goal).filter(Goal.id == goal_id).first()
    if not goal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Career goal with ID {goal_id} not found."
        )

    questions = db.query(OverallGoalEvaluationQuestion).filter(
        OverallGoalEvaluationQuestion.goal_id == goal_id
    ).order_by(OverallGoalEvaluationQuestion.order_index.asc()).all()

    results = []
    for q in questions:
        try:
            raw_options = json.loads(q.options_json)
            options = [OverallQuestionOption(id=opt["id"], text=opt["text"]) for opt in raw_options]
        except Exception:
            options = []

        # Parse integrated skills
        raw_skills = [s.strip() for s in q.integrated_skills.split(",") if s.strip()]

        results.append(
            OverallQuestionResponse(
                id=q.id,
                goal_id=q.goal_id,
                question_text=q.question_text,
                question_type=q.question_type,
                integrated_skills=raw_skills,
                options=options,
                scenario_context=q.scenario_context,
                order_index=q.order_index
            )
        )
    return results


def submit_goal_overall_evaluation(
    db: Session,
    user_id: int,
    goal_id: int,
    request: OverallEvaluationSubmissionRequest
) -> OverallEvaluationResultResponse:
    """
    Grade cross-skill integration answers, compute readiness level, categorize strong vs weak skills,
    generate architectural insights and pre-interview recommendations, and persist to database.
    """
    goal = db.query(Goal).filter(Goal.id == goal_id).first()
    if not goal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Career goal with ID {goal_id} not found."
        )

    questions = db.query(OverallGoalEvaluationQuestion).filter(
        OverallGoalEvaluationQuestion.goal_id == goal_id
    ).order_by(OverallGoalEvaluationQuestion.order_index.asc()).all()

    if not questions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No overall evaluation questions configured for goal ID {goal_id}."
        )

    total_questions = len(questions)
    score = 0
    strong_skills_set = set()
    weak_skills_set = set()
    question_breakdown: List[OverallQuestionResult] = []

    for q in questions:
        selected_option = request.answers.get(str(q.id)) or request.answers.get(q.id)
        is_correct = (selected_option == q.correct_option) if selected_option else False

        raw_skills = [s.strip() for s in q.integrated_skills.split(",") if s.strip()]

        if is_correct:
            score += 1
            for sk in raw_skills:
                strong_skills_set.add(sk)
        else:
            for sk in raw_skills:
                weak_skills_set.add(sk)

        question_breakdown.append(
            OverallQuestionResult(
                question_id=q.id,
                question_text=q.question_text,
                integrated_skills=raw_skills,
                selected_option=selected_option,
                correct_option=q.correct_option,
                is_correct=is_correct,
                explanation=q.explanation
            )
        )

    strong_skills = sorted(list(strong_skills_set - weak_skills_set))
    if not strong_skills and score > 0:
        strong_skills = sorted(list(strong_skills_set))

    weak_skills = sorted(list(weak_skills_set))

    percentage = round((score / total_questions) * 100)

    # Readiness Classification
    if percentage >= 85:
        readiness_level = "Advanced / Exceptional"
        readiness_summary = (
            f"Exceptional cross-skill architecture command! You achieved {score}/{total_questions} ({percentage}%), "
            f"proving comprehensive end-to-end fluency across the entire {goal.title} discipline."
        )
    elif percentage >= 70:
        readiness_level = "Interview-Ready"
        readiness_summary = (
            f"Solid professional readiness! You scored {score}/{total_questions} ({percentage}%), showing strong cross-skill "
            f"integration capability and readiness to tackle technical hiring rounds."
        )
    elif percentage >= 50:
        readiness_level = "Developing"
        readiness_summary = (
            f"Good baseline integration with growth opportunities. You scored {score}/{total_questions} ({percentage}%). "
            f"Reinforcing end-to-end debugging and data flow handoffs will elevate you to interview-ready status."
        )
    else:
        readiness_level = "Beginner"
        readiness_summary = (
            f"Foundational review recommended. You scored {score}/{total_questions} ({percentage}%). "
            f"Take time to review individual skill interactions before facing demanding multi-stage technical interviews."
        )

    # Cross-Skill Architectural Insights
    cross_skill_insights = []
    if "React" in strong_skills and "FastAPI" in strong_skills:
        cross_skill_insights.append("Strong full-stack synchronization between frontend reactive state and ASGI asynchronous endpoints.")
    if "Database" in weak_skills or "SQLAlchemy" in weak_skills:
        cross_skill_insights.append("Database query optimization and relational schema transactions require closer attention.")
    if "Marketing" in strong_skills and "Finance" in strong_skills:
        cross_skill_insights.append("Sound grasp of customer unit economics (LTV:CAC) and its direct impact on operating cash flow.")
    if not cross_skill_insights:
        cross_skill_insights.append(
            f"Demonstrated competence in {len(strong_skills)} integrated skill domains with {len(weak_skills)} targeted focus areas."
        )

    # Actionable Recommendations before Final Interview Prep
    recommendations = []
    if weak_skills:
        recommendations.append(f"Revisit key practical exercises for: {', '.join(weak_skills)}.")
    recommendations.append("Practice explaining end-to-end system architectures on a whiteboard or diagramming canvas.")
    recommendations.append("Formulate 2-3 production case studies using the STAR method (Situation, Task, Action, Result).")
    if percentage >= 70:
        recommendations.append("You are ready to advance directly to the Final 15 Must-Know Interview Questions.")
    else:
        recommendations.append("Review the question breakdown explanations below before proceeding to the final interview preparation.")

    now = datetime.now(timezone.utc)

    # Persist record in database
    eval_record = UserGoalEvaluation(
        user_id=user_id,
        goal_id=goal_id,
        score=score,
        total_questions=total_questions,
        percentage=percentage,
        readiness_level=readiness_level,
        readiness_summary=readiness_summary,
        answers_json=json.dumps(request.answers),
        strong_skills_json=json.dumps(strong_skills),
        skills_needing_improvement_json=json.dumps(weak_skills),
        cross_skill_insights_json=json.dumps(cross_skill_insights),
        recommendations_json=json.dumps(recommendations),
        completed_at=now
    )
    db.add(eval_record)
    db.commit()
    db.refresh(eval_record)

    return OverallEvaluationResultResponse(
        id=eval_record.id,
        goal_id=goal.id,
        goal_title=goal.title,
        score=score,
        total_questions=total_questions,
        percentage=percentage,
        readiness_level=readiness_level,
        readiness_summary=readiness_summary,
        strong_skills=strong_skills,
        skills_needing_improvement=weak_skills,
        cross_skill_insights=cross_skill_insights,
        recommendations=recommendations,
        question_breakdown=question_breakdown,
        completed_at=now
    )


def get_latest_user_goal_evaluation(
    db: Session,
    user_id: int,
    goal_id: int
) -> Optional[OverallEvaluationResultResponse]:
    """
    Retrieve the user's latest overall evaluation report for a goal.
    """
    goal = db.query(Goal).filter(Goal.id == goal_id).first()
    if not goal:
        return None

    record = db.query(UserGoalEvaluation).filter(
        UserGoalEvaluation.user_id == user_id,
        UserGoalEvaluation.goal_id == goal_id
    ).order_by(UserGoalEvaluation.completed_at.desc()).first()

    if not record:
        return None

    # Reconstruct question breakdown
    questions = db.query(OverallGoalEvaluationQuestion).filter(
        OverallGoalEvaluationQuestion.goal_id == goal_id
    ).order_by(OverallGoalEvaluationQuestion.order_index.asc()).all()

    try:
        user_answers = json.loads(record.answers_json)
    except Exception:
        user_answers = {}

    question_breakdown = []
    for q in questions:
        selected_option = user_answers.get(str(q.id)) or user_answers.get(q.id)
        is_correct = (selected_option == q.correct_option) if selected_option else False
        raw_skills = [s.strip() for s in q.integrated_skills.split(",") if s.strip()]

        question_breakdown.append(
            OverallQuestionResult(
                question_id=q.id,
                question_text=q.question_text,
                integrated_skills=raw_skills,
                selected_option=selected_option,
                correct_option=q.correct_option,
                is_correct=is_correct,
                explanation=q.explanation
            )
        )

    try:
        strong_skills = json.loads(record.strong_skills_json)
    except Exception:
        strong_skills = []

    try:
        weak_skills = json.loads(record.skills_needing_improvement_json)
    except Exception:
        weak_skills = []

    try:
        cross_skill_insights = json.loads(record.cross_skill_insights_json)
    except Exception:
        cross_skill_insights = []

    try:
        recommendations = json.loads(record.recommendations_json)
    except Exception:
        recommendations = []

    return OverallEvaluationResultResponse(
        id=record.id,
        goal_id=goal.id,
        goal_title=goal.title,
        score=record.score,
        total_questions=record.total_questions,
        percentage=record.percentage,
        readiness_level=record.readiness_level,
        readiness_summary=record.readiness_summary,
        strong_skills=strong_skills,
        skills_needing_improvement=weak_skills,
        cross_skill_insights=cross_skill_insights,
        recommendations=recommendations,
        question_breakdown=question_breakdown,
        completed_at=record.completed_at
    )

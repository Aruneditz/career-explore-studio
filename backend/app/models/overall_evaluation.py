from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database.database import Base


def utc_now():
    return datetime.now(timezone.utc)


class OverallGoalEvaluationQuestion(Base):
    __tablename__ = "overall_goal_evaluation_questions"

    id = Column(Integer, primary_key=True, index=True)
    goal_id = Column(Integer, ForeignKey("goals.id", ondelete="CASCADE"), nullable=False, index=True)
    question_text = Column(Text, nullable=False)
    question_type = Column(String(60), default="cross_skill_integration", nullable=False)
    # Comma-separated or JSON list of skills tested (e.g. "React, FastAPI, Database")
    integrated_skills = Column(String(200), nullable=False)
    options_json = Column(Text, nullable=False)  # JSON: [{"id": "A", "text": "..."}, ...]
    correct_option = Column(String(10), nullable=False)  # "A", "B", "C", "D"
    explanation = Column(Text, nullable=False)
    scenario_context = Column(Text, nullable=True)
    order_index = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)

    # Relationships
    goal = relationship("Goal", back_populates="overall_evaluation_questions")

    def __repr__(self):
        return f"<OverallGoalEvaluationQuestion id={self.id} goal_id={self.goal_id} type={self.question_type}>"


class UserGoalEvaluation(Base):
    __tablename__ = "user_goal_evaluations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    goal_id = Column(Integer, ForeignKey("goals.id", ondelete="CASCADE"), nullable=False, index=True)
    score = Column(Integer, nullable=False)
    total_questions = Column(Integer, nullable=False)
    percentage = Column(Integer, nullable=False)
    # "Beginner" (<50%), "Developing" (50-69%), "Interview-Ready" (70-84%), "Advanced / Exceptional" (>=85%)
    readiness_level = Column(String(50), nullable=False)
    readiness_summary = Column(Text, nullable=False)
    answers_json = Column(Text, nullable=False)  # JSON: {"1": "A", "2": "C"}
    strong_skills_json = Column(Text, nullable=False)  # JSON: ["React", "FastAPI"]
    skills_needing_improvement_json = Column(Text, nullable=False)  # JSON: ["Database"]
    cross_skill_insights_json = Column(Text, nullable=False)  # JSON list
    recommendations_json = Column(Text, nullable=False)  # JSON list
    completed_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)

    # Relationships
    user = relationship("User", back_populates="goal_evaluations")
    goal = relationship("Goal", back_populates="user_evaluations")

    def __repr__(self):
        return f"<UserGoalEvaluation id={self.id} user_id={self.user_id} goal_id={self.goal_id} readiness={self.readiness_level}>"

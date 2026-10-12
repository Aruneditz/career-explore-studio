from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from sqlalchemy.orm import relationship
from app.database.database import Base


def utc_now():
    return datetime.now(timezone.utc)


class Goal(Base):
    __tablename__ = "goals"

    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String(100), unique=True, index=True, nullable=False)
    title = Column(String(150), nullable=False)
    category = Column(String(50), nullable=False, index=True)  # Technical, Business, Marketing, Design, etc.
    description = Column(Text, nullable=False)
    career_relevance = Column(Text, nullable=False)
    icon = Column(String(50), default="Target", nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)

    # Relationships
    skills = relationship("Skill", back_populates="goal", cascade="all, delete-orphan", order_by="Skill.order_index")
    user_selections = relationship("UserGoalSelection", back_populates="goal", cascade="all, delete-orphan")
    overall_evaluation_questions = relationship("OverallGoalEvaluationQuestion", back_populates="goal", cascade="all, delete-orphan", order_by="OverallGoalEvaluationQuestion.order_index")
    user_evaluations = relationship("UserGoalEvaluation", back_populates="goal", cascade="all, delete-orphan")
    final_interview_questions = relationship("GoalFinalInterviewQuestion", back_populates="goal", cascade="all, delete-orphan", order_by="GoalFinalInterviewQuestion.question_number")

    def __repr__(self):
        return f"<Goal id={self.id} title={self.title} category={self.category}>"

from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database.database import Base


def utc_now():
    return datetime.now(timezone.utc)


class EvaluationQuestion(Base):
    __tablename__ = "evaluation_questions"

    id = Column(Integer, primary_key=True, index=True)
    skill_id = Column(Integer, ForeignKey("skills.id", ondelete="CASCADE"), nullable=False, index=True)
    question_text = Column(Text, nullable=False)
    question_type = Column(String(50), default="conceptual", nullable=False)  # "conceptual", "practical", "problem_solving", "understanding"
    options_json = Column(Text, nullable=False)  # JSON string: [{"id": "A", "text": "..."}, ...]
    correct_option = Column(String(10), nullable=False)  # "A", "B", "C", "D"
    explanation = Column(Text, nullable=False)
    topic_area = Column(String(100), nullable=True)  # Categorization for strong/weak area diagnostics
    order_index = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)

    # Relationships
    skill = relationship("Skill", back_populates="evaluation_questions")

    def __repr__(self):
        return f"<EvaluationQuestion id={self.id} skill_id={self.skill_id} topic_area={self.topic_area}>"


class UserSkillEvaluation(Base):
    __tablename__ = "user_skill_evaluations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    skill_id = Column(Integer, ForeignKey("skills.id", ondelete="CASCADE"), nullable=False, index=True)
    score = Column(Integer, nullable=False)
    total_questions = Column(Integer, nullable=False)
    percentage = Column(Integer, nullable=False)
    answers_json = Column(Text, nullable=False)  # JSON string: {"1": "A", "2": "C"}
    strong_areas_json = Column(Text, nullable=False)  # JSON string: ["Topic 1", "Topic 2"]
    weak_areas_json = Column(Text, nullable=False)  # JSON string: ["Topic 3"]
    feedback_summary = Column(Text, nullable=False)
    improvement_suggestions_json = Column(Text, nullable=False)  # JSON string list
    completed_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)

    # Relationships
    user = relationship("User", back_populates="evaluations")
    skill = relationship("Skill", back_populates="user_evaluations")

    def __repr__(self):
        return f"<UserSkillEvaluation id={self.id} user_id={self.user_id} skill_id={self.skill_id} score={self.score}/{self.total_questions}>"

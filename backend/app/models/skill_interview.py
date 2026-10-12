from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database.database import Base


def utc_now():
    return datetime.now(timezone.utc)


class SkillInterviewQuestion(Base):
    __tablename__ = "skill_interview_questions"

    id = Column(Integer, primary_key=True, index=True)
    skill_id = Column(Integer, ForeignKey("skills.id", ondelete="CASCADE"), nullable=False, index=True)
    question = Column(Text, nullable=False)
    difficulty = Column(String(20), default="Basic", nullable=False)  # "Basic", "Intermediate", "Advanced"
    category = Column(String(50), default="Conceptual", nullable=False)  # "Conceptual", "Practical Scenario", "Architecture", etc.
    expected_answer = Column(Text, nullable=False)
    simple_syntax = Column(Text, nullable=True)
    small_example = Column(Text, nullable=True)
    explanation = Column(Text, nullable=False)
    practical_scenario = Column(Text, nullable=True)
    tips_for_answering = Column(Text, nullable=False)
    common_mistakes = Column(Text, nullable=False)
    order_index = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)

    # Relationships
    skill = relationship("Skill", back_populates="interview_questions")

    def __repr__(self):
        return f"<SkillInterviewQuestion id={self.id} skill_id={self.skill_id} difficulty={self.difficulty}>"

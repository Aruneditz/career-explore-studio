from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database.database import Base


def utc_now():
    return datetime.now(timezone.utc)


class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    goal_id = Column(Integer, ForeignKey("goals.id", ondelete="CASCADE"), nullable=False, index=True)
    slug = Column(String(100), index=True, nullable=False)
    name = Column(String(150), nullable=False)
    category = Column(String(50), default="Core", nullable=False)
    description = Column(Text, nullable=False)
    is_technical = Column(Boolean, default=True, nullable=False)
    order_index = Column(Integer, default=0, nullable=False)

    # Detailed Skill Overview Fields (Section 12)
    what_is_it = Column(Text, nullable=True)
    why_important = Column(Text, nullable=True)
    where_used = Column(Text, nullable=True)
    benefits = Column(Text, nullable=True)
    challenges = Column(Text, nullable=True)
    prerequisites = Column(Text, nullable=True)
    career_relevance = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)

    # Relationships
    goal = relationship("Goal", back_populates="skills")
    topics = relationship("Topic", back_populates="skill", cascade="all, delete-orphan", order_by="Topic.order_index")
    practical_items = relationship("PracticalContent", back_populates="skill", cascade="all, delete-orphan", order_by="PracticalContent.order_index")
    user_progress_entries = relationship("UserSkillProgress", back_populates="skill", cascade="all, delete-orphan")
    evaluation_questions = relationship("EvaluationQuestion", back_populates="skill", cascade="all, delete-orphan", order_by="EvaluationQuestion.order_index")
    user_evaluations = relationship("UserSkillEvaluation", back_populates="skill", cascade="all, delete-orphan")
    interview_questions = relationship("SkillInterviewQuestion", back_populates="skill", cascade="all, delete-orphan", order_by="SkillInterviewQuestion.order_index")

    def __repr__(self):
        return f"<Skill id={self.id} name={self.name} goal_id={self.goal_id}>"

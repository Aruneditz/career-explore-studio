from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from app.database.database import Base


def utc_now():
    return datetime.now(timezone.utc)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now, nullable=False)

    # Relationships with cascade deletion
    goal_selections = relationship("UserGoalSelection", back_populates="user", cascade="all, delete-orphan")
    topic_progress_entries = relationship("UserTopicProgress", back_populates="user", cascade="all, delete-orphan")
    skill_progress_entries = relationship("UserSkillProgress", back_populates="user", cascade="all, delete-orphan")
    evaluations = relationship("UserSkillEvaluation", back_populates="user", cascade="all, delete-orphan")
    goal_evaluations = relationship("UserGoalEvaluation", back_populates="user", cascade="all, delete-orphan")
    interview_practices = relationship("UserInterviewPractice", back_populates="user", cascade="all, delete-orphan")
    certificates = relationship("UserCertificate", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User id={self.id} email={self.email} name={self.name}>"

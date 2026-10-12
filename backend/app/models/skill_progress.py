from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database.database import Base


def utc_now():
    return datetime.now(timezone.utc)


class UserSkillProgress(Base):
    __tablename__ = "user_skill_progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    skill_id = Column(Integer, ForeignKey("skills.id", ondelete="CASCADE"), nullable=False, index=True)
    status = Column(String(30), default="in_progress", nullable=False)  # "not_started", "in_progress", "completed"
    is_completed = Column(Boolean, default=False, nullable=False)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    progress_percentage = Column(Integer, default=0, nullable=False)
    practical_reviewed = Column(Boolean, default=False, nullable=False)
    interview_reviewed = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now, nullable=False)

    __table_args__ = (
        UniqueConstraint("user_id", "skill_id", name="uq_user_skill_progress_user_skill"),
    )

    # Relationships
    user = relationship("User", back_populates="skill_progress_entries")
    skill = relationship("Skill", back_populates="user_progress_entries")

    def __repr__(self):
        return f"<UserSkillProgress user_id={self.user_id} skill_id={self.skill_id} is_completed={self.is_completed}>"

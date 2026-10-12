from datetime import datetime, timezone
from sqlalchemy import Column, Integer, Boolean, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database.database import Base


def utc_now():
    return datetime.now(timezone.utc)


class UserGoalSelection(Base):
    __tablename__ = "user_goal_selections"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    goal_id = Column(Integer, ForeignKey("goals.id", ondelete="CASCADE"), nullable=False, index=True)
    is_active = Column(Boolean, default=True, nullable=False)
    selected_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)

    __table_args__ = (
        UniqueConstraint("user_id", "goal_id", name="uq_user_goal"),
    )

    # Relationships
    user = relationship("User", back_populates="goal_selections")
    goal = relationship("Goal", back_populates="user_selections")

    def __repr__(self):
        return f"<UserGoalSelection user_id={self.user_id} goal_id={self.goal_id} is_active={self.is_active}>"

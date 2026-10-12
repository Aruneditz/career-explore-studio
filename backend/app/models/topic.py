from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database.database import Base


def utc_now():
    return datetime.now(timezone.utc)


class Topic(Base):
    __tablename__ = "topics"

    id = Column(Integer, primary_key=True, index=True)
    skill_id = Column(Integer, ForeignKey("skills.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(150), nullable=False)
    description = Column(Text, nullable=False)
    order_index = Column(Integer, default=0, nullable=False)
    is_must_know = Column(Boolean, default=False, nullable=False)  # Important / Must-Know flag
    estimated_minutes = Column(Integer, default=15, nullable=False)
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)

    # Relationships
    skill = relationship("Skill", back_populates="topics")
    progress_records = relationship("UserTopicProgress", back_populates="topic", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Topic id={self.id} title={self.title} is_must_know={self.is_must_know}>"

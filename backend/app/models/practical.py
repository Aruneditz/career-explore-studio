from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database.database import Base


def utc_now():
    return datetime.now(timezone.utc)


class PracticalContent(Base):
    __tablename__ = "practical_content"

    id = Column(Integer, primary_key=True, index=True)
    skill_id = Column(Integer, ForeignKey("skills.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(150), nullable=False)
    content_type = Column(String(50), nullable=False)  # "code_syntax", "exercise", "scenario", "case_study"
    language = Column(String(30), nullable=True)  # "javascript", "python", "html", "css", etc.
    code_snippet = Column(Text, nullable=True)  # Syntax/code for technical skills
    explanation = Column(Text, nullable=False)
    real_world_context = Column(Text, nullable=False)
    activity_prompt = Column(Text, nullable=True)
    solution_or_guide = Column(Text, nullable=True)
    order_index = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)

    # Relationships
    skill = relationship("Skill", back_populates="practical_items")

    def __repr__(self):
        return f"<PracticalContent id={self.id} title={self.title} content_type={self.content_type}>"

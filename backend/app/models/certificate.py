import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database.database import Base


def utc_now():
    return datetime.now(timezone.utc)


def generate_certificate_id(cert_type: str = "SKILL") -> str:
    """Generate a clean, professional, unique certificate identifier."""
    prefix = "CES-SKILL" if cert_type.lower() == "skill" else "CES-COURSE"
    unique_suffix = uuid.uuid4().hex[:8].upper()
    year = datetime.now(timezone.utc).year
    return f"{prefix}-{year}-{unique_suffix}"


class UserCertificate(Base):
    __tablename__ = "user_certificates"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    certificate_id = Column(String(64), unique=True, nullable=False, index=True)
    certificate_type = Column(String(30), default="skill", nullable=False)  # "skill" or "goal"
    skill_id = Column(Integer, ForeignKey("skills.id", ondelete="SET NULL"), nullable=True, index=True)
    goal_id = Column(Integer, ForeignKey("goals.id", ondelete="SET NULL"), nullable=True, index=True)
    title = Column(String(255), nullable=False)
    recipient_name = Column(String(150), nullable=False)
    issued_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)
    status = Column(String(30), default="issued", nullable=False)  # "issued", "revoked"
    metadata_json = Column(Text, nullable=True)  # JSON string of scores, topics count, career path, etc.

    __table_args__ = (
        UniqueConstraint("user_id", "skill_id", name="uq_user_certificate_user_skill"),
    )

    # Relationships
    user = relationship("User", back_populates="certificates")
    skill = relationship("Skill")
    goal = relationship("Goal")

    def __repr__(self):
        return f"<UserCertificate id={self.id} cert_id={self.certificate_id} recipient={self.recipient_name} title={self.title}>"

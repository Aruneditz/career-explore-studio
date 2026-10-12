from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database.database import Base


def utc_now():
    return datetime.now(timezone.utc)


class GoalFinalInterviewQuestion(Base):
    """
    Capstone Interview Preparation Question model (Sections 21 & 22).
    Represents one of the EXACTLY 15 MUST-KNOW INTERVIEW QUESTIONS for a career goal.
    """
    __tablename__ = "goal_final_interview_questions"

    id = Column(Integer, primary_key=True, index=True)
    goal_id = Column(Integer, ForeignKey("goals.id", ondelete="CASCADE"), nullable=False, index=True)
    question_number = Column(Integer, nullable=False)  # Exactly 1 to 15
    question = Column(Text, nullable=False)
    # Categories: "Core Fundamentals", "Practical & Scenario-Based", "Advanced & Problem Solving"
    category = Column(String(60), default="Core Fundamentals", nullable=False, index=True)
    why_asked = Column(Text, nullable=False)
    interviewer_looking_for = Column(Text, nullable=False)
    detailed_answer = Column(Text, nullable=False)
    simple_syntax = Column(Text, nullable=True)
    small_example = Column(Text, nullable=True)
    code_or_practical_example = Column(Text, nullable=True)
    scenario_example = Column(Text, nullable=True)
    response_structure_star = Column(Text, nullable=False)
    what_not_to_say = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)

    # Relationships
    goal = relationship("Goal", back_populates="final_interview_questions")
    practice_records = relationship("UserInterviewPractice", back_populates="question", cascade="all, delete-orphan")

    __table_args__ = (
        UniqueConstraint("goal_id", "question_number", name="uq_goal_question_number"),
    )

    def __repr__(self):
        return f"<GoalFinalInterviewQuestion id={self.id} goal_id={self.goal_id} num={self.question_number} cat={self.category}>"


class UserInterviewPractice(Base):
    """
    Tracks which final interview questions the user has marked as practiced / understood.
    """
    __tablename__ = "user_interview_practices"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    question_id = Column(Integer, ForeignKey("goal_final_interview_questions.id", ondelete="CASCADE"), nullable=False, index=True)
    is_practiced = Column(Boolean, default=True, nullable=False)
    practiced_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)

    # Relationships
    user = relationship("User", back_populates="interview_practices")
    question = relationship("GoalFinalInterviewQuestion", back_populates="practice_records")

    __table_args__ = (
        UniqueConstraint("user_id", "question_id", name="uq_user_interview_practice"),
    )

    def __repr__(self):
        return f"<UserInterviewPractice user_id={self.user_id} q_id={self.question_id} practiced={self.is_practiced}>"

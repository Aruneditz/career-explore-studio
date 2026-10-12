from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, example="Alex Developer")
    email: EmailStr = Field(..., example="alex@example.com")


class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=100, example="securePassword123")


class UserLogin(BaseModel):
    email: EmailStr = Field(..., example="alex@example.com")
    password: str = Field(..., min_length=1, example="securePassword123")


class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class UserProfileUpdateRequest(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)


class UserProfileSummaryResponse(BaseModel):
    user: UserResponse
    active_goal_id: Optional[int] = None
    active_goal_title: Optional[str] = None
    active_goal_slug: Optional[str] = None
    active_goal_category: Optional[str] = None
    skills_completed: int = 0
    total_skills: int = 0
    skill_completion_percentage: int = 0
    topics_completed: int = 0
    total_topics: int = 0
    readiness_level: Optional[str] = None
    interview_practiced_count: int = 0
    achievements_count: int = 0
    total_achievements: int = 8

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class TokenPayload(BaseModel):
    sub: str | None = None
    exp: int | None = None

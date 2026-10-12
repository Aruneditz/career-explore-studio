from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.ai import (
    AIAskRequest,
    AIAskResponse,
    AISuggestionResponse,
)
from app.services import ai_service

router = APIRouter(prefix="", tags=["AI Assistant"])


@router.post("/ask", response_model=AIAskResponse)
def ask_ai(
    request: AIAskRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Ask Career Explore Studio AI Mentor.
    Incorporates candidate's active goal, completed skills, and topic context.
    Protected endpoint.
    """
    if not request.prompt.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Prompt query cannot be empty."
        )

    return ai_service.ask_ai_mentor(db, current_user.id, request)


@router.get("/suggestions", response_model=AISuggestionResponse)
def get_suggestions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retrieve dynamically suggested prompt chips for the authenticated user.
    """
    suggestions = ai_service.get_suggested_prompts(db, current_user.id)
    return AISuggestionResponse(suggestions=suggestions)

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas.auth import UserCreate, UserLogin, UserResponse, Token, UserProfileUpdateRequest, UserProfileSummaryResponse
from app.schemas.common import MessageResponse
from app.services import auth_service, dashboard_service
from app.core.security import create_access_token
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter()


@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
def register_user(user_in: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user account and return an access token.
    """
    user = auth_service.create_user(db, user_in)
    access_token = create_access_token(subject=user.id)
    return Token(
        access_token=access_token,
        token_type="bearer",
        user=user
    )


@router.post("/login", response_model=Token)
def login_user(credentials: UserLogin, db: Session = Depends(get_db)):
    """
    Authenticate user with email and password, returning an access token.
    """
    user = auth_service.authenticate_user(db, credentials)
    access_token = create_access_token(subject=user.id)
    return Token(
        access_token=access_token,
        token_type="bearer",
        user=user
    )


@router.get("/me", response_model=UserResponse)
def read_current_user(current_user: User = Depends(get_current_user)):
    """
    Get current authenticated user profile.
    Protected endpoint requiring valid Bearer token.
    """
    return current_user


@router.post("/logout", response_model=MessageResponse)
def logout_user():
    """
    Acknowledge user logout (tokens are stateless JWTs, cleared on the client).
    """
    return MessageResponse(message="Successfully logged out.")


@router.get("/profile-summary", response_model=UserProfileSummaryResponse)
def get_user_profile_summary(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get user profile summary including active goal, skills completed, and achievements count (Phase 12).
    """
    return dashboard_service.get_user_profile_summary(db, user_id=current_user.id)


@router.put("/profile", response_model=UserResponse)
def update_profile(
    request: UserProfileUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update current user profile name (Phase 12).
    """
    return dashboard_service.update_user_profile(db, user_id=current_user.id, request=request)

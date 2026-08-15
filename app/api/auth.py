# app/api/auth.py
"""
ARGUS Authentication API
=========================
Handles login, registration, and user management endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.services.user_service import (
    authenticate_user,
    create_user,
    get_all_users,
    get_user_by_username,
    update_user_role
)
from app.core.security import create_access_token
from app.core.dependencies import get_current_user, require_role
from app.database.models import User
from app.schemas.user import UserCreate, UserResponse, TokenResponse, LoginRequest
from app.core.logger import setup_logger

logger = setup_logger(__name__)
router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login", response_model=TokenResponse)
def login(body: LoginRequest, db: Session = Depends(get_db)):
    """
    Authenticate user and return JWT token.
    Send username and password, receive token.
    """
    user = authenticate_user(db, body.username, body.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )

    token = create_access_token(
        data={"sub": user.username, "role": user.role}
    )

    return {
        "access_token": token,
        "token_type":   "bearer",
        "username":     user.username,
        "role":         user.role
    }

@router.post("/register", response_model=UserResponse)
def register(
    body: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin"))
):
    """
    Register a new user.
    Only admins can create new accounts.
    """
    existing = get_user_by_username(db, body.username)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )

    user = create_user(
        db,
        username=body.username,
        email=body.email,
        password=body.password,
        role=body.role
    )
    return user

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    """Get current logged in user profile"""
    return current_user

@router.get("/users")
def list_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin"))
):
    """List all users — admin only"""
    return get_all_users(db)

@router.put("/users/{user_id}/role")
def change_user_role(
    user_id: int,
    role: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin"))
):
    """Update user role — admin only"""
    update_user_role(db, user_id, role)
    return {"message": f"User {user_id} role updated to {role}"}
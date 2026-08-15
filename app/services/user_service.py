# app/services/user_service.py
"""
ARGUS User Service
==================
Handles user management database operations.
"""

from sqlalchemy.orm import Session
from app.database.models import User
from app.core.security import hash_password, verify_password
from app.core.logger import setup_logger

logger = setup_logger(__name__)

def create_user(db: Session, username: str, email: str, password: str, role: str = "readonly") -> User:
    """Create a new user with hashed password"""
    user = User(
        username=username,
        email=email,
        hashed_password=hash_password(password),
        role=role
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    logger.info(f"User created: {username} with role {role}")
    return user

def get_user_by_username(db: Session, username: str) -> User:
    """Get user by username"""
    return db.query(User).filter(User.username == username).first()

def get_all_users(db: Session) -> list[dict]:
    """Get all users"""
    users = db.query(User).all()
    return [user.to_dict() for user in users]

def authenticate_user(db: Session, username: str, password: str):
    """
    Verify username and password.
    Returns user if valid, None if invalid.
    """
    user = get_user_by_username(db, username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

def update_user_role(db: Session, user_id: int, role: str) -> None:
    """Update a user's role — admin only"""
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.role = role
        db.commit()
        logger.info(f"User {user_id} role updated to {role}")
# app/core/security.py
"""
ARGUS Security Module
=====================
Handles password hashing and JWT token creation/verification.

Why bcrypt for passwords:
- bcrypt is a one-way hash — you cannot reverse it
- Even if database is stolen, passwords are safe
- bcrypt is slow by design — makes brute force attacks harder

Why JWT for tokens:
- Stateless — server does not store sessions
- Self-contained — token carries user info inside
- Signed — server can verify token was not tampered with
"""

from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import settings
from app.core.logger import setup_logger

logger = setup_logger(__name__)

# Password hashing context using bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """
    Hash a plain text password using bcrypt.
    The hash is different every time even for same password
    because bcrypt adds a random salt.
    """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against its hash.
    Returns True if match, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a signed JWT token containing user data.

    The token contains:
    - sub: username (subject)
    - role: user role
    - exp: expiry timestamp

    The token is signed with SECRET_KEY so any
    tampering will be detected on verification.
    """
    to_encode = data.copy()

    expire = datetime.utcnow() + (
        expires_delta or
        timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})

    token = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    logger.info(f"Token created for user: {data.get('sub')}")
    return token

def decode_token(token: str) -> Optional[dict]:
    """
    Decode and verify a JWT token.
    Returns the payload if valid, None if invalid or expired.
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        return payload
    except JWTError as e:
        logger.warning(f"Token verification failed: {e}")
        return None
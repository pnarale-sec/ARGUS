# app/database/connection.py
"""
ARGUS Database Connection
=========================
SQLAlchemy engine and session management.

Key concepts:
- Engine:  the connection to the database
- Session: the workspace for database operations
           like a shopping cart — add items, then checkout (commit)
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.core.config import settings
from app.core.logger import setup_logger

logger = setup_logger(__name__)

# Build PostgreSQL connection URL
# Format: postgresql://user:password@host:port/dbname
DATABASE_URL = (
    f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}"
    f"@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
)

# Engine — manages the actual database connection pool
# pool_size=10 means max 10 connections kept open
# echo=False means don't print every SQL query
engine = create_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    echo=False
)

# SessionLocal — factory for creating new sessions
# autocommit=False means we control when to save
# autoflush=False means we control when to sync
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def get_db() -> Session:
    """
    Dependency function that provides a database session.
    Used by FastAPI routes via Depends().

    Automatically closes session after request is complete.
    This is the recommended FastAPI + SQLAlchemy pattern.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """
    Creates all tables defined in models.py.
    Called once when application starts.
    """
    from app.database.models import Base
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables initialized via SQLAlchemy")
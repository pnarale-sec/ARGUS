# app/services/log_service.py
"""
ARGUS Log Service
=================
All log database operations using SQLAlchemy ORM.

Before (raw SQL):
    cursor.execute("SELECT * FROM logs")
    rows = cursor.fetchall()

After (SQLAlchemy):
    logs = db.query(Log).all()

Much cleaner. Much safer.
"""

from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database.models import Log
from app.core.logger import setup_logger

logger = setup_logger(__name__)

def insert_log(db: Session, log: dict) -> None:
    """Insert a single parsed log into database"""
    db_log = Log(
        timestamp=log["timestamp"],
        level=log["level"],
        message=log["message"],
        source=log["source"]
    )
    db.add(db_log)
    db.commit()
    db.refresh(db_log)

def get_all_logs(db: Session) -> list[dict]:
    """Retrieve all logs ordered by newest first"""
    logs = db.query(Log).order_by(Log.id.desc()).all()
    return [log.to_dict() for log in logs]

def get_logs_by_level(db: Session, level: str) -> list[dict]:
    """Retrieve logs filtered by severity level"""
    logs = (
        db.query(Log)
        .filter(Log.level == level)
        .order_by(Log.id.desc())
        .all()
    )
    return [log.to_dict() for log in logs]

def get_log_stats(db: Session) -> dict:
    """Get log count statistics for dashboard cards"""
    total    = db.query(func.count(Log.id)).scalar()
    info     = db.query(func.count(Log.id)).filter(Log.level == "INFO").scalar()
    warning  = db.query(func.count(Log.id)).filter(Log.level == "WARNING").scalar()
    error    = db.query(func.count(Log.id)).filter(Log.level == "ERROR").scalar()
    critical = db.query(func.count(Log.id)).filter(Log.level == "CRITICAL").scalar()
    sources  = db.query(func.count(func.distinct(Log.source))).scalar()

    return {
        "total":    total,
        "info":     info,
        "warning":  warning,
        "error":    error,
        "critical": critical,
        "sources":  sources
    }
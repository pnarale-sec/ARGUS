# app/api/logs.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.services.log_service import (
    get_all_logs,
    get_logs_by_level,
    get_log_stats
)
from app.core.logger import setup_logger

logger = setup_logger(__name__)
router = APIRouter(prefix="/api/logs", tags=["Logs"])

@router.get("")
def fetch_all_logs(db: Session = Depends(get_db)):
    logs = get_all_logs(db)
    return {"total": len(logs), "logs": logs}

@router.get("/stats")
def fetch_log_stats(db: Session = Depends(get_db)):
    return get_log_stats(db)

@router.get("/level/{level}")
def fetch_logs_by_level(level: str, db: Session = Depends(get_db)):
    logs = get_logs_by_level(db, level.upper())
    return {"level": level.upper(), "total": len(logs), "logs": logs}
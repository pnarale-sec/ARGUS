# app/api/logs.py
"""
ARGUS Log API Routes
====================
Handles all HTTP endpoints related to logs.

Why separate route files:
- Each file has one clear responsibility
- Easy to find and modify specific routes
- Scales cleanly as we add more endpoints
"""

from fastapi import APIRouter
from app.services.log_service import (
    get_all_logs,
    get_logs_by_level,
    get_log_stats
)
from app.schemas.log import LogListResponse
from app.core.logger import setup_logger

logger = setup_logger(__name__)

# APIRouter instead of app — these get registered in main.py
router = APIRouter(prefix="/api/logs", tags=["Logs"])

@router.get("", response_model=LogListResponse)
def fetch_all_logs():
    """
    Get all logs from database.
    Returns total count and list of logs.
    """
    logger.info("Fetching all logs")
    logs = get_all_logs()
    return {"total": len(logs), "logs": logs}

@router.get("/level/{level}")
def fetch_logs_by_level(level: str):
    """
    Get logs filtered by severity level.
    Level can be: INFO, WARNING, ERROR, CRITICAL
    """
    logs = get_logs_by_level(level.upper())
    return {
        "level": level.upper(),
        "total": len(logs),
        "logs":  logs
    }

@router.get("/stats")
def fetch_log_stats():
    """
    Get log statistics for dashboard cards.
    Returns count per severity level.
    """
    return get_log_stats()
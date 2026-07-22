# app/api/health.py
"""
ARGUS Health Check API
======================
Simple endpoint to verify the system is running.

Why health checks:
- Monitoring tools ping this to verify the system is alive
- Docker and Kubernetes use health checks to restart crashed services
- Load balancers use it to route traffic only to healthy instances
"""

from fastapi import APIRouter
from app.core.config import settings
from datetime import datetime

router = APIRouter(tags=["Health"])

@router.get("/health")
def health_check():
    """
    Returns system health status.
    Always returns 200 OK if the API is running.
    """
    return {
        "status":  "healthy",
        "app":     settings.APP_NAME,
        "version": settings.APP_VERSION,
        "time":    datetime.now().isoformat()
    }
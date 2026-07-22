# app/api/alerts.py
"""
ARGUS Alert API Routes
======================
Handles all HTTP endpoints related to alerts.
"""

from fastapi import APIRouter
from app.services.alert_service import (
    get_all_alerts,
    update_alert_status,
    get_alert_stats
)
from app.schemas.alert import AlertListResponse, AlertStatusUpdate
from app.core.logger import setup_logger

logger = setup_logger(__name__)

router = APIRouter(prefix="/api/alerts", tags=["Alerts"])

@router.get("", response_model=AlertListResponse)
def fetch_all_alerts():
    """Get all security alerts ordered by newest first"""
    logger.info("Fetching all alerts")
    alerts = get_all_alerts()
    return {"total": len(alerts), "alerts": alerts}

@router.put("/{alert_id}/status")
def change_alert_status(alert_id: int, body: AlertStatusUpdate):
    """
    Update the status of an alert.
    Valid statuses: NEW, ACKNOWLEDGED, RESOLVED
    """
    update_alert_status(alert_id, body.status)
    return {
        "message": f"Alert {alert_id} updated to {body.status}"
    }

@router.get("/stats")
def fetch_alert_stats():
    """Get alert statistics for dashboard"""
    return get_alert_stats()
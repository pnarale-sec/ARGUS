# app/api/alerts.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.database.models import User
from app.services.alert_service import (
    get_all_alerts,
    update_alert_status,
    get_alert_stats
)
from app.schemas.alert import AlertStatusUpdate
from app.core.dependencies import require_role
from app.core.logger import setup_logger

logger = setup_logger(__name__)
router = APIRouter(prefix="/api/alerts", tags=["Alerts"])

@router.get("")
def fetch_all_alerts(db: Session = Depends(get_db)):
    """Public — dashboard reads this"""
    alerts = get_all_alerts(db)
    return {"total": len(alerts), "alerts": alerts}

@router.put("/{alert_id}/status")
def change_alert_status(
    alert_id: int,
    body: AlertStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin", "analyst"))
):
    """Protected — only admin and analyst can update"""
    update_alert_status(db, alert_id, body.status)
    return {"message": f"Alert {alert_id} updated to {body.status}"}

@router.get("/stats")
def fetch_alert_stats(db: Session = Depends(get_db)):
    """Public — dashboard reads this"""
    return get_alert_stats(db)
# app/api/alerts.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.services.alert_service import (
    get_all_alerts,
    update_alert_status,
    get_alert_stats
)
from app.schemas.alert import AlertStatusUpdate
from app.core.logger import setup_logger

logger = setup_logger(__name__)
router = APIRouter(prefix="/api/alerts", tags=["Alerts"])

@router.get("")
def fetch_all_alerts(db: Session = Depends(get_db)):
    alerts = get_all_alerts(db)
    return {"total": len(alerts), "alerts": alerts}

@router.put("/{alert_id}/status")
def change_alert_status(
    alert_id: int,
    body: AlertStatusUpdate,
    db: Session = Depends(get_db)
):
    update_alert_status(db, alert_id, body.status)
    return {"message": f"Alert {alert_id} updated to {body.status}"}

@router.get("/stats")
def fetch_alert_stats(db: Session = Depends(get_db)):
    return get_alert_stats(db)
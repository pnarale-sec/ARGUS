# app/services/alert_service.py
"""
ARGUS Alert Service
===================
All alert database operations using SQLAlchemy ORM.
"""

from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database.models import Alert
from app.core.logger import setup_logger

logger = setup_logger(__name__)

def insert_alert(db: Session, alert: dict) -> None:
    """Insert a new alert into database"""
    db_alert = Alert(
        rule_name=alert["rule_name"],
        description=alert["description"],
        severity=alert["severity"],
        source_ip=alert["source_ip"],
        log_ids=alert["log_ids"],
        status=alert["status"]
    )
    db.add(db_alert)
    db.commit()
    logger.info(f"Alert inserted: {alert['rule_name']}")

def get_all_alerts(db: Session) -> list[dict]:
    """Retrieve all alerts ordered by newest first"""
    alerts = (
        db.query(Alert)
        .order_by(Alert.created_at.desc())
        .all()
    )
    return [alert.to_dict() for alert in alerts]

def update_alert_status(db: Session, alert_id: int, status: str) -> None:
    """Update the status of an alert"""
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if alert:
        alert.status = status
        db.commit()
        logger.info(f"Alert {alert_id} status updated to {status}")

def get_alert_stats(db: Session) -> dict:
    """Get alert statistics for dashboard"""
    total      = db.query(func.count(Alert.id)).scalar()
    critical   = db.query(func.count(Alert.id)).filter(Alert.severity == "CRITICAL").scalar()
    high       = db.query(func.count(Alert.id)).filter(Alert.severity == "HIGH").scalar()
    medium     = db.query(func.count(Alert.id)).filter(Alert.severity == "MEDIUM").scalar()
    new_alerts = db.query(func.count(Alert.id)).filter(Alert.status == "NEW").scalar()

    return {
        "total":      total,
        "critical":   critical,
        "high":       high,
        "medium":     medium,
        "new_alerts": new_alerts
    }
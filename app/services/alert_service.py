# app/services/alert_service.py
"""
ARGUS Alert Service
===================
Handles all alert-related database operations.
"""

from app.database.connection import get_connection, release_connection
from app.core.logger import setup_logger

logger = setup_logger(__name__)

def insert_alert(alert: dict) -> None:
    """Insert a new alert into database"""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO alerts
                (rule_name, description, severity,
                 source_ip, log_ids, status)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            alert["rule_name"],
            alert["description"],
            alert["severity"],
            alert["source_ip"],
            alert["log_ids"],
            alert["status"]
        ))
        conn.commit()
        cursor.close()
        logger.info(f"Alert inserted: {alert['rule_name']}")
    except Exception as e:
        conn.rollback()
        logger.error(f"Failed to insert alert: {e}")
        raise
    finally:
        release_connection(conn)

def get_all_alerts() -> list[dict]:
    """Retrieve all alerts ordered by newest first"""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, rule_name, description, severity,
                   source_ip, log_ids, status, created_at
            FROM alerts
            ORDER BY created_at DESC
        """)
        rows = cursor.fetchall()
        cursor.close()
        return [
            {
                "id":          row[0],
                "rule_name":   row[1],
                "description": row[2],
                "severity":    row[3],
                "source_ip":   row[4],
                "log_ids":     row[5],
                "status":      row[6],
                "created_at":  str(row[7])
            }
            for row in rows
        ]
    except Exception as e:
        logger.error(f"Failed to fetch alerts: {e}")
        raise
    finally:
        release_connection(conn)

def update_alert_status(alert_id: int, status: str) -> None:
    """Update the status of an alert"""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE alerts SET status = %s WHERE id = %s
        """, (status, alert_id))
        conn.commit()
        cursor.close()
        logger.info(f"Alert {alert_id} status updated to {status}")
    except Exception as e:
        conn.rollback()
        logger.error(f"Failed to update alert status: {e}")
        raise
    finally:
        release_connection(conn)

def get_alert_stats() -> dict:
    """Get alert count statistics for dashboard"""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT
                COUNT(*) as total,
                COUNT(CASE WHEN severity = 'CRITICAL' THEN 1 END) as critical,
                COUNT(CASE WHEN severity = 'HIGH'     THEN 1 END) as high,
                COUNT(CASE WHEN severity = 'MEDIUM'   THEN 1 END) as medium,
                COUNT(CASE WHEN status = 'NEW'        THEN 1 END) as new_alerts
            FROM alerts
        """)
        row = cursor.fetchone()
        cursor.close()
        return {
            "total":      row[0],
            "critical":   row[1],
            "high":       row[2],
            "medium":     row[3],
            "new_alerts": row[4]
        }
    except Exception as e:
        logger.error(f"Failed to fetch alert stats: {e}")
        raise
    finally:
        release_connection(conn)
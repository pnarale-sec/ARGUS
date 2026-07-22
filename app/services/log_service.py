# app/services/log_service.py
"""
ARGUS Log Service
=================
Handles all log-related database operations.

Why a service layer:
- Keeps API routes thin and clean
- Business logic is reusable across multiple routes
- Easier to test in isolation
- Separation of concerns
"""

from app.database.connection import get_connection, release_connection
from app.core.logger import setup_logger

logger = setup_logger(__name__)

def insert_log(log: dict) -> None:
    """Insert a single parsed log into database"""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO logs (timestamp, level, message, source)
            VALUES (%s, %s, %s, %s)
        """, (
            log["timestamp"],
            log["level"],
            log["message"],
            log["source"]
        ))
        conn.commit()
        cursor.close()
    except Exception as e:
        conn.rollback()
        logger.error(f"Failed to insert log: {e}")
        raise
    finally:
        release_connection(conn)

def get_all_logs() -> list[dict]:
    """Retrieve all logs ordered by newest first"""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, timestamp, level, message, source
            FROM logs
            ORDER BY id DESC
        """)
        rows = cursor.fetchall()
        cursor.close()
        return [
            {
                "id":        row[0],
                "timestamp": row[1],
                "level":     row[2],
                "message":   row[3],
                "source":    row[4]
            }
            for row in rows
        ]
    except Exception as e:
        logger.error(f"Failed to fetch logs: {e}")
        raise
    finally:
        release_connection(conn)

def get_logs_by_level(level: str) -> list[dict]:
    """Retrieve logs filtered by severity level"""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, timestamp, level, message, source
            FROM logs
            WHERE level = %s
            ORDER BY id DESC
        """, (level,))
        rows = cursor.fetchall()
        cursor.close()
        return [
            {
                "id":        row[0],
                "timestamp": row[1],
                "level":     row[2],
                "message":   row[3],
                "source":    row[4]
            }
            for row in rows
        ]
    except Exception as e:
        logger.error(f"Failed to fetch logs by level: {e}")
        raise
    finally:
        release_connection(conn)

def get_log_stats() -> dict:
    """Get log count statistics for dashboard cards"""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT
                COUNT(*) as total,
                COUNT(CASE WHEN level = 'INFO'     THEN 1 END) as info,
                COUNT(CASE WHEN level = 'WARNING'  THEN 1 END) as warning,
                COUNT(CASE WHEN level = 'ERROR'    THEN 1 END) as error,
                COUNT(CASE WHEN level = 'CRITICAL' THEN 1 END) as critical,
                COUNT(DISTINCT source) as sources
            FROM logs
        """)
        row = cursor.fetchone()
        cursor.close()
        return {
            "total":    row[0],
            "info":     row[1],
            "warning":  row[2],
            "error":    row[3],
            "critical": row[4],
            "sources":  row[5]
        }
    except Exception as e:
        logger.error(f"Failed to fetch log stats: {e}")
        raise
    finally:
        release_connection(conn)
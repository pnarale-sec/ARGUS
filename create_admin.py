# create_admin.py
"""
Run once to create the default admin user.
    python create_admin.py
"""

from app.database.connection import init_db, SessionLocal
from app.services.user_service import create_user, get_user_by_username
from app.core.logger import setup_logger

logger = setup_logger(__name__)

def main():
    init_db()
    db = SessionLocal()

    try:
        # Check if admin already exists
        existing = get_user_by_username(db, "admin")
        if existing:
            logger.info("Admin user already exists")
            return

        # Create admin
        create_user(
            db,
            username="admin",
            email="admin@argus.local",
            password="Admin@123",
            role="admin"
        )

        # Create analyst
        create_user(
            db,
            username="analyst",
            email="analyst@argus.local",
            password="Analyst@123",
            role="analyst"
        )

        # Create readonly
        create_user(
            db,
            username="viewer",
            email="viewer@argus.local",
            password="Viewer@123",
            role="readonly"
        )

        logger.info("Default users created successfully")
        logger.info("Admin:   admin / Admin@123")
        logger.info("Analyst: analyst / Analyst@123")
        logger.info("Viewer:  viewer / Viewer@123")

    finally:
        db.close()

main()
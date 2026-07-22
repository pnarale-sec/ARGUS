# app/database/connection.py
"""
ARGUS Database Connection
=========================
Manages PostgreSQL connection pool.

Why connection pooling:
- Opening a database connection is expensive (takes time)
- A pool keeps connections open and reuses them
- Much faster than opening/closing for every query
- Handles multiple simultaneous requests properly
"""

import psycopg2
from psycopg2 import pool
from app.core.config import settings
from app.core.logger import setup_logger

logger = setup_logger(__name__)

# Connection pool — keeps 1 to 10 connections open
connection_pool = None

def init_connection_pool():
    """
    Creates the connection pool when app starts.
    Called once at startup — not for every request.
    """
    global connection_pool

    try:
        connection_pool = psycopg2.pool.ThreadedConnectionPool(
            minconn=1,   # minimum open connections
            maxconn=10,  # maximum open connections
            host=settings.DB_HOST,
            port=settings.DB_PORT,
            dbname=settings.DB_NAME,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD
        )
        logger.info("Database connection pool initialized")
    except Exception as e:
        logger.error(f"Failed to initialize connection pool: {e}")
        raise

def get_connection():
    """
    Gets a connection from the pool.
    Use this instead of creating new connections.
    """
    if connection_pool is None:
        init_connection_pool()
    return connection_pool.getconn()

def release_connection(conn):
    """
    Returns connection back to pool for reuse.
    Always call this after you are done with a connection.
    """
    if connection_pool and conn:
        connection_pool.putconn(conn)

def init_db():
    """
    Creates all database tables if they don't exist.
    Called once when application starts.
    """
    conn = get_connection()
    try:
        cursor = conn.cursor()

        # Logs table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS logs (
                id        SERIAL PRIMARY KEY,
                timestamp TEXT,
                level     TEXT,
                message   TEXT,
                source    TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Alerts table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS alerts (
                id          SERIAL PRIMARY KEY,
                rule_name   TEXT,
                description TEXT,
                severity    TEXT,
                source_ip   TEXT,
                log_ids     TEXT,
                status      TEXT DEFAULT 'NEW',
                created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.commit()
        cursor.close()
        logger.info("Database tables initialized successfully")

    except Exception as e:
        conn.rollback()
        logger.error(f"Database initialization failed: {e}")
        raise
    finally:
        # Always release connection back to pool
        release_connection(conn)
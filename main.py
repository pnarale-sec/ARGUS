# main.py
"""
ARGUS SIEM — Main Application Entry Point
==========================================
This file:
1. Creates the FastAPI application
2. Registers all API routers
3. Sets up CORS middleware
4. Serves the static dashboard
5. Initializes the database on startup

Why everything connects here:
- Single entry point makes the app easy to understand
- Adding new features = adding one new router import
- Clean separation from business logic
"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.logger import setup_logger
from app.database.connection import init_connection_pool, init_db
from app.api import logs, alerts, health

import os

logger = setup_logger(__name__)

# ── Create FastAPI app ────────────────────────────────
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Advanced Real-time Guard & Unified Security System"
)

# ── CORS Middleware ───────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Static files (dashboard) ──────────────────────────
static_path = os.path.join(os.path.dirname(__file__), "static")
app.mount(
    "/static",
    StaticFiles(directory=static_path),
    name="static"
)

# ── Register API routers ──────────────────────────────
app.include_router(logs.router)
app.include_router(alerts.router)
app.include_router(health.router)

# ── Startup event ─────────────────────────────────────
@app.on_event("startup")
def startup():
    """
    Runs when server starts.
    Initialize database connection pool and tables.
    """
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    init_connection_pool()
    init_db()
    logger.info("ARGUS is ready")

# ── Dashboard route ───────────────────────────────────
@app.get("/")
def dashboard():
    """Serve the main dashboard HTML file"""
    return FileResponse(
        os.path.join(static_path, "dashboard.html")
    )
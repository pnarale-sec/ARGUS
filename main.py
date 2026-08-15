# main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer

from app.core.config import settings
from app.core.logger import setup_logger
from app.database.connection import init_db
from app.api import logs, alerts, health, auth

import os

logger = setup_logger(__name__)

# HTTPBearer tells Swagger to show a Bearer token input box
security = HTTPBearer()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Advanced Real-time Guard & Unified Security System"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files
static_path = os.path.join(os.path.dirname(__file__), "static")
app.mount(
    "/static",
    StaticFiles(directory=static_path),
    name="static"
)

# Register routers
app.include_router(auth.router)
app.include_router(logs.router)
app.include_router(alerts.router)
app.include_router(health.router)

@app.on_event("startup")
def startup():
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    init_db()
    logger.info("ARGUS is ready")

@app.get("/")
def dashboard():
    return FileResponse(
        os.path.join(static_path, "dashboard.html")
    )
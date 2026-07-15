from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os

try:
    from .database import init_db, get_all_logs, get_logs_by_level
except ImportError:
    from database import init_db, get_all_logs, get_logs_by_level

app = FastAPI(title="ARGUS SIEM API", version="1.0")

# Allow browser to talk to API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files from static folder
static_path = os.path.join(os.path.dirname(__file__), "..", "static")
app.mount("/static", StaticFiles(directory=static_path), name="static")

@app.on_event("startup")
def startup():
    init_db()

@app.get("/")
def home():
    return FileResponse(os.path.join(static_path, "dashboard.html"))

@app.get("/logs")
def fetch_logs():
    logs = get_all_logs()
    return {"total": len(logs), "logs": logs}

@app.get("/logs/level/{level}")
def fetch_logs_by_level(level: str):
    logs = get_logs_by_level(level.upper())
    return {"level": level.upper(), "total": len(logs), "logs": logs}
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from database import (init_db, init_alerts_table,
                      get_all_logs, get_logs_by_level,
                      get_all_alerts, update_alert_status)
import os

app = FastAPI(title="ARGUS SIEM API", version="2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

static_path = os.path.join(
    os.path.dirname(__file__), "..", "static")
app.mount("/static",
          StaticFiles(directory=static_path),
          name="static")

@app.on_event("startup")
def startup():
    init_db()
    init_alerts_table()

@app.get("/")
def home():
    return FileResponse(
        os.path.join(static_path, "dashboard.html"))

@app.get("/logs")
def fetch_logs():
    logs = get_all_logs()
    return {"total": len(logs), "logs": logs}

@app.get("/logs/level/{level}")
def fetch_logs_by_level(level: str):
    logs = get_logs_by_level(level.upper())
    return {"level": level.upper(),
            "total": len(logs), "logs": logs}

@app.get("/alerts")
def fetch_alerts():
    alerts = get_all_alerts()
    return {"total": len(alerts), "alerts": alerts}

@app.put("/alerts/{alert_id}/status")
def change_alert_status(alert_id: int, status: str):
    update_alert_status(alert_id, status)
    return {"message": f"Alert {alert_id} "
                       f"updated to {status}"}
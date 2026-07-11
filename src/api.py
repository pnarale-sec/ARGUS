from fastapi import FastAPI
from database import init_db, get_all_logs, get_logs_by_level

app = FastAPI(title=" SIEM API", version="1.0")

@app.on_event("startup")
def startup():
    init_db()

@app.get("/")
def home():
    return {
        "message":"SIEM is running"
    }

@app.get("/logs")
def fetch_logs():
    logs = get_all_logs()
    return {"total": len(logs), "logs": logs}

@app.get("/logs/level/{level}")
def fetch_logs_by_level(level: str):
    logs = get_logs_by_level(level.upper())
    return {"level": level.upper(), "total": len(logs), "logs": logs}
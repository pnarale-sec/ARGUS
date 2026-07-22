# app/detection/rule_engine.py
"""
ARGUS Detection Rule Engine
============================
Analyzes logs and generates alerts when threats are detected.

Why a dedicated detection module:
- Phase 8 will expand this to 10+ rules
- Each rule is an isolated function — easy to add/remove
- Rules can be tested independently
"""

import re
from app.services.alert_service import insert_alert
from app.core.config import settings
from app.core.logger import setup_logger

logger = setup_logger(__name__)

def extract_ip(message: str) -> str:
    """Extract first IP address found in message"""
    match = re.search(
        r'\b(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\b',
        message
    )
    return match.group(1) if match else "unknown"

def extract_username(message: str) -> str:
    """Extract username from log message"""
    for pattern in [
        r'user\s+(\w+)',
        r'for\s+user\s+(\w+)',
        r'username[:\s]+(\w+)'
    ]:
        match = re.search(pattern, message, re.IGNORECASE)
        if match:
            return match.group(1)
    return "unknown"

# ── RULE 1 — Brute Force ──────────────────────────────
def detect_brute_force(logs: list[dict]) -> list[dict]:
    """
    Detects brute force login attacks.
    Triggers when same IP has 5+ failed logins.
    """
    alerts  = []
    tracker = {}

    FAILED_KEYWORDS = [
        "failed login", "failed password",
        "authentication failure", "invalid password",
        "login failed"
    ]

    for log in logs:
        msg = log["message"].lower()
        if any(kw in msg for kw in FAILED_KEYWORDS):
            ip = extract_ip(log["message"])
            if ip not in tracker:
                tracker[ip] = {
                    "count":    0,
                    "log_ids":  [],
                    "username": extract_username(log["message"])
                }
            tracker[ip]["count"] += 1
            tracker[ip]["log_ids"].append(str(log["id"]))

    for ip, data in tracker.items():
        if data["count"] >= settings.BRUTE_FORCE_THRESHOLD:
            alerts.append({
                "rule_name":   "BRUTE_FORCE_DETECTED",
                "description": (
                    f"Brute force attack from {ip}. "
                    f"{data['count']} failed attempts "
                    f"for user '{data['username']}'."
                ),
                "severity":  "HIGH",
                "source_ip": ip,
                "log_ids":   ",".join(data["log_ids"]),
                "status":    "NEW"
            })
            logger.warning(
                f"Brute force detected from {ip} "
                f"— {data['count']} attempts"
            )

    return alerts

# ── RULE 2 — Error Storm ──────────────────────────────
def detect_error_storm(logs: list[dict]) -> list[dict]:
    """
    Detects error storms.
    Triggers when same source has 3+ ERROR logs.
    """
    alerts  = []
    tracker = {}

    for log in logs:
        if log["level"] == "ERROR":
            src = log["source"]
            if src not in tracker:
                tracker[src] = {"count": 0, "log_ids": []}
            tracker[src]["count"] += 1
            tracker[src]["log_ids"].append(str(log["id"]))

    for src, data in tracker.items():
        if data["count"] >= settings.ERROR_STORM_THRESHOLD:
            alerts.append({
                "rule_name":   "ERROR_STORM_DETECTED",
                "description": (
                    f"{data['count']} ERROR events from '{src}'."
                ),
                "severity":  "MEDIUM",
                "source_ip": "N/A",
                "log_ids":   ",".join(data["log_ids"]),
                "status":    "NEW"
            })
            logger.warning(
                f"Error storm in {src} — {data['count']} errors"
            )

    return alerts

# ── RULE 3 — Suspicious Keywords ─────────────────────
def detect_suspicious_keywords(logs: list[dict]) -> list[dict]:
    """
    Detects known attack keywords in log messages.
    """
    alerts = []

    KEYWORDS = [
        "sql injection", "xss", "cross-site",
        "unauthorized", "privilege escalation",
        "root access", "malware", "exploit",
        "backdoor", "reverse shell",
        "command injection", "directory traversal"
    ]

    for log in logs:
        msg = log["message"].lower()
        for kw in KEYWORDS:
            if kw in msg:
                alerts.append({
                    "rule_name":   "SUSPICIOUS_KEYWORD",
                    "description": (
                        f"Keyword '{kw}' in log "
                        f"#{log['id']}: "
                        f"{log['message'][:100]}"
                    ),
                    "severity":  "CRITICAL",
                    "source_ip": extract_ip(log["message"]),
                    "log_ids":   str(log["id"]),
                    "status":    "NEW"
                })
                logger.warning(
                    f"Suspicious keyword '{kw}' "
                    f"in log #{log['id']}"
                )
                break

    return alerts

# ── MAIN ENGINE ───────────────────────────────────────
def run_rule_engine(logs: list[dict]) -> int:
    """
    Runs all detection rules against a list of logs.
    Saves generated alerts to database.
    Returns total number of alerts generated.
    """
    logger.info(
        f"Rule engine starting — analyzing {len(logs)} logs"
    )

    all_alerts = (
        detect_brute_force(logs) +
        detect_error_storm(logs) +
        detect_suspicious_keywords(logs)
    )

    for alert in all_alerts:
        insert_alert(alert)

    logger.info(
        f"Rule engine complete — {len(all_alerts)} alerts generated"
    )
    return len(all_alerts)
# app/detection/rule_engine.py
"""
ARGUS Detection Rule Engine — Phase 8
======================================
10 detection rules covering the most common attack patterns.

Each rule is an isolated function that:
1. Receives the full log list
2. Analyzes for specific patterns
3. Returns a list of alert dictionaries

Why isolated functions:
- Easy to add new rules without touching existing ones
- Each rule can be tested independently
- Rules can be enabled/disabled individually

MITRE ATT&CK mappings included for each rule.
"""

import re
from sqlalchemy.orm import Session
from app.services.alert_service import insert_alert
from app.core.config import settings
from app.core.logger import setup_logger

logger = setup_logger(__name__)


# ── HELPER FUNCTIONS ──────────────────────────────────

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
        r'by\s+user\s+(\w+)',
        r'username[:\s]+(\w+)'
    ]:
        match = re.search(pattern, message, re.IGNORECASE)
        if match:
            return match.group(1)
    return "unknown"

def extract_port(message: str) -> str:
    """Extract port number from log message"""
    match = re.search(r'port\s+(\d+)', message, re.IGNORECASE)
    return match.group(1) if match else "unknown"


# ── RULE 1 — Brute Force ─────────────────────────────
# MITRE ATT&CK: T1110 — Brute Force

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
                    f"for user '{data['username']}'. "
                    f"MITRE ATT&CK: T1110"
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


# ── RULE 2 — Error Storm ─────────────────────────────

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
                    f"{data['count']} ERROR events "
                    f"from source '{src}'. "
                    f"Possible system instability."
                ),
                "severity":  "MEDIUM",
                "source_ip": "N/A",
                "log_ids":   ",".join(data["log_ids"]),
                "status":    "NEW"
            })

    return alerts


# ── RULE 3 — Port Scan ───────────────────────────────
# MITRE ATT&CK: T1046 — Network Service Scanning

def detect_port_scan(logs: list[dict]) -> list[dict]:
    """
    Detects port scanning activity.
    Triggers when same IP connects to 4+ different ports.
    """
    alerts  = []
    tracker = {}

    PORT_KEYWORDS = [
        "port scan", "connection attempt",
        "connect to port", "connection to port"
    ]

    for log in logs:
        msg = log["message"].lower()
        if any(kw in msg for kw in PORT_KEYWORDS):
            ip = extract_ip(log["message"])
            if ip not in tracker:
                tracker[ip] = {"ports": set(), "log_ids": []}
            port = extract_port(log["message"])
            tracker[ip]["ports"].add(port)
            tracker[ip]["log_ids"].append(str(log["id"]))

    for ip, data in tracker.items():
        if len(data["ports"]) >= 4:
            alerts.append({
                "rule_name":   "PORT_SCAN_DETECTED",
                "description": (
                    f"Port scan from {ip}. "
                    f"Ports targeted: {', '.join(data['ports'])}. "
                    f"MITRE ATT&CK: T1046"
                ),
                "severity":  "HIGH",
                "source_ip": ip,
                "log_ids":   ",".join(data["log_ids"]),
                "status":    "NEW"
            })
            logger.warning(
                f"Port scan from {ip} "
                f"— {len(data['ports'])} ports"
            )

    return alerts


# ── RULE 4 — SQL Injection ───────────────────────────
# MITRE ATT&CK: T1190 — Exploit Public-Facing Application

def detect_sql_injection(logs: list[dict]) -> list[dict]:
    """
    Detects SQL injection attempts in log messages.
    """
    alerts = []

    SQL_PATTERNS = [
        r"union\s+select",
        r"or\s+1\s*=\s*1",
        r"drop\s+table",
        r"insert\s+into",
        r"select\s+\*\s+from",
        r"--\s*$",
        r";\s*drop",
        r"xp_cmdshell",
        r"exec\s*\(",
        r"sleep\s*\(\d+\)"
    ]

    for log in logs:
        msg = log["message"].lower()
        for pattern in SQL_PATTERNS:
            if re.search(pattern, msg):
                alerts.append({
                    "rule_name":   "SQL_INJECTION_DETECTED",
                    "description": (
                        f"SQL injection pattern in log #{log['id']}: "
                        f"{log['message'][:120]}. "
                        f"MITRE ATT&CK: T1190"
                    ),
                    "severity":  "CRITICAL",
                    "source_ip": extract_ip(log["message"]),
                    "log_ids":   str(log["id"]),
                    "status":    "NEW"
                })
                logger.warning(
                    f"SQL injection in log #{log['id']}"
                )
                break

    return alerts


# ── RULE 5 — XSS ─────────────────────────────────────
# MITRE ATT&CK: T1059.007

def detect_xss(logs: list[dict]) -> list[dict]:
    """
    Detects cross-site scripting attempts.
    """
    alerts = []

    XSS_PATTERNS = [
        r"<script",
        r"javascript:",
        r"onerror\s*=",
        r"onload\s*=",
        r"alert\s*\(",
        r"document\.cookie",
        r"eval\s*\(",
        r"<img[^>]+src\s*=\s*['\"]?javascript"
    ]

    for log in logs:
        msg = log["message"].lower()
        for pattern in XSS_PATTERNS:
            if re.search(pattern, msg):
                alerts.append({
                    "rule_name":   "XSS_DETECTED",
                    "description": (
                        f"XSS pattern in log #{log['id']}: "
                        f"{log['message'][:120]}. "
                        f"MITRE ATT&CK: T1059.007"
                    ),
                    "severity":  "HIGH",
                    "source_ip": extract_ip(log["message"]),
                    "log_ids":   str(log["id"]),
                    "status":    "NEW"
                })
                logger.warning(f"XSS detected in log #{log['id']}")
                break

    return alerts


# ── RULE 6 — Privilege Escalation ────────────────────
# MITRE ATT&CK: T1068

def detect_privilege_escalation(logs: list[dict]) -> list[dict]:
    """
    Detects privilege escalation attempts.
    """
    alerts = []

    PRIV_KEYWORDS = [
        "privilege escalation",
        "sudo su",
        "sudo -i",
        "chmod 777",
        "chown root",
        "unauthorized sudo",
        "root access",
        "setuid",
        "sudo bash",
        "sudo sh"
    ]

    for log in logs:
        msg = log["message"].lower()
        for kw in PRIV_KEYWORDS:
            if kw in msg:
                alerts.append({
                    "rule_name":   "PRIVILEGE_ESCALATION_DETECTED",
                    "description": (
                        f"Privilege escalation attempt by "
                        f"'{extract_username(log['message'])}': "
                        f"{log['message'][:120]}. "
                        f"MITRE ATT&CK: T1068"
                    ),
                    "severity":  "CRITICAL",
                    "source_ip": extract_ip(log["message"]),
                    "log_ids":   str(log["id"]),
                    "status":    "NEW"
                })
                logger.warning(
                    f"Privilege escalation in log #{log['id']}"
                )
                break

    return alerts


# ── RULE 7 — Directory Traversal ─────────────────────
# MITRE ATT&CK: T1083

def detect_directory_traversal(logs: list[dict]) -> list[dict]:
    """
    Detects directory traversal / path traversal attacks.
    """
    alerts = []

    TRAVERSAL_PATTERNS = [
        r"\.\./",
        r"\.\.\\",
        r"%2e%2e%2f",
        r"%252e%252e",
        r"/etc/passwd",
        r"/etc/shadow",
        r"directory traversal",
        r"path traversal"
    ]

    for log in logs:
        msg = log["message"].lower()
        for pattern in TRAVERSAL_PATTERNS:
            if re.search(pattern, msg):
                alerts.append({
                    "rule_name":   "DIRECTORY_TRAVERSAL_DETECTED",
                    "description": (
                        f"Directory traversal attempt in log "
                        f"#{log['id']}: "
                        f"{log['message'][:120]}. "
                        f"MITRE ATT&CK: T1083"
                    ),
                    "severity":  "HIGH",
                    "source_ip": extract_ip(log["message"]),
                    "log_ids":   str(log["id"]),
                    "status":    "NEW"
                })
                logger.warning(
                    f"Directory traversal in log #{log['id']}"
                )
                break

    return alerts


# ── RULE 8 — Data Exfiltration ───────────────────────
# MITRE ATT&CK: T1041

def detect_data_exfiltration(logs: list[dict]) -> list[dict]:
    """
    Detects potential data exfiltration.
    Triggers on large data transfers to external IPs.
    """
    alerts = []

    EXFIL_KEYWORDS = [
        "large data transfer",
        "unusual outbound",
        "data exfiltration",
        "large upload",
        "gb sent",
        "mb transfer",
        "mb sent"
    ]

    for log in logs:
        msg = log["message"].lower()
        for kw in EXFIL_KEYWORDS:
            if kw in msg:
                alerts.append({
                    "rule_name":   "DATA_EXFILTRATION_DETECTED",
                    "description": (
                        f"Possible data exfiltration: "
                        f"{log['message'][:120]}. "
                        f"MITRE ATT&CK: T1041"
                    ),
                    "severity":  "CRITICAL",
                    "source_ip": extract_ip(log["message"]),
                    "log_ids":   str(log["id"]),
                    "status":    "NEW"
                })
                logger.warning(
                    f"Data exfiltration in log #{log['id']}"
                )
                break

    return alerts


# ── RULE 9 — Repeated 404 ────────────────────────────
# MITRE ATT&CK: T1595 — Active Scanning

def detect_repeated_404(logs: list[dict]) -> list[dict]:
    """
    Detects web scanners and recon activity.
    Triggers when same IP causes 4+ 404 errors.
    """
    alerts  = []
    tracker = {}

    for log in logs:
        msg = log["message"].lower()
        if "404" in msg:
            ip = extract_ip(log["message"])
            if ip not in tracker:
                tracker[ip] = {"count": 0, "log_ids": []}
            tracker[ip]["count"] += 1
            tracker[ip]["log_ids"].append(str(log["id"]))

    for ip, data in tracker.items():
        if data["count"] >= 4:
            alerts.append({
                "rule_name":   "WEB_SCANNER_DETECTED",
                "description": (
                    f"Possible web scanner from {ip}. "
                    f"{data['count']} 404 errors. "
                    f"Recon activity suspected. "
                    f"MITRE ATT&CK: T1595"
                ),
                "severity":  "MEDIUM",
                "source_ip": ip,
                "log_ids":   ",".join(data["log_ids"]),
                "status":    "NEW"
            })
            logger.warning(
                f"Web scanner from {ip} "
                f"— {data['count']} 404s"
            )

    return alerts


# ── RULE 10 — Suspicious Keywords ────────────────────

def detect_suspicious_keywords(logs: list[dict]) -> list[dict]:
    """
    Detects known attack keywords not covered by other rules.
    """
    alerts = []

    KEYWORDS = [
        "malware", "exploit", "backdoor",
        "reverse shell", "command injection",
        "ransomware", "keylogger", "rootkit"
    ]

    for log in logs:
        msg = log["message"].lower()
        for kw in KEYWORDS:
            if kw in msg:
                alerts.append({
                    "rule_name":   "SUSPICIOUS_KEYWORD_DETECTED",
                    "description": (
                        f"Suspicious keyword '{kw}' in "
                        f"log #{log['id']}: "
                        f"{log['message'][:120]}"
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

def run_rule_engine(db: Session, logs: list[dict]) -> int:
    """
    Runs all 10 detection rules against the log list.
    Saves all generated alerts to database.
    Returns total number of alerts generated.
    """
    logger.info(
        f"Rule engine starting — analyzing {len(logs)} logs "
        f"with 10 detection rules"
    )

    all_alerts = (
        detect_brute_force(logs)         +
        detect_error_storm(logs)         +
        detect_port_scan(logs)           +
        detect_sql_injection(logs)       +
        detect_xss(logs)                 +
        detect_privilege_escalation(logs)+
        detect_directory_traversal(logs) +
        detect_data_exfiltration(logs)   +
        detect_repeated_404(logs)        +
        detect_suspicious_keywords(logs)
    )

    for alert in all_alerts:
        insert_alert(db, alert)

    logger.info(
        f"Rule engine complete — "
        f"{len(all_alerts)} alerts generated"
    )
    return len(all_alerts)
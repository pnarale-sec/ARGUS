import re
from database import insert_alert

# ══════════════════════════════════════════
# RULE ENGINE — ARGUS Detection System
# ══════════════════════════════════════════

# How many failed logins before alert
BRUTE_FORCE_THRESHOLD = 5

def extract_ip(message):
    """Extract IP address from log message"""
    pattern = r'\b(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\b'
    match = re.search(pattern, message)
    return match.group(1) if match else "unknown"

def extract_username(message):
    """Extract username from log message"""
    patterns = [
        r'user\s+(\w+)',
        r'for\s+user\s+(\w+)',
        r'username[:\s]+(\w+)'
    ]
    for pattern in patterns:
        match = re.search(pattern, message, re.IGNORECASE)
        if match:
            return match.group(1)
    return "unknown"

# ══════════════════════════════════════════
# RULE 1 — Brute Force Detection
# ══════════════════════════════════════════

def detect_brute_force(logs):
    """
    Detect brute force attacks.
    Rule: Same IP fails login more than 5 times
    """
    alerts = []

    # Count failed logins per IP
    failed_logins = {}

    for log in logs:
        message = log["message"].lower()
        is_failed = (
            "failed login" in message or
            "failed password" in message or
            "authentication failure" in message or
            "invalid password" in message or
            "login failed" in message
        )

        if is_failed:
            ip = extract_ip(log["message"])
            if ip not in failed_logins:
                failed_logins[ip] = {
                    "count":   0,
                    "log_ids": [],
                    "user":    extract_username(log["message"])
                }
            failed_logins[ip]["count"]   += 1
            failed_logins[ip]["log_ids"].append(str(log["id"]))

    # Check if any IP exceeded threshold
    for ip, data in failed_logins.items():
        if data["count"] >= BRUTE_FORCE_THRESHOLD:
            alert = {
                "rule_name":   "BRUTE_FORCE_DETECTED",
                "description": (
                    f"Brute force attack detected from IP {ip}. "
                    f"{data['count']} failed login attempts "
                    f"for user '{data['user']}'."
                ),
                "severity":    "HIGH",
                "source_ip":   ip,
                "log_ids":     ",".join(data["log_ids"]),
                "status":      "NEW"
            }
            alerts.append(alert)
            print(f"[ALERT] Brute force detected from {ip} "
                  f"— {data['count']} attempts")

    return alerts

# ══════════════════════════════════════════
# RULE 2 — Multiple Errors Detection
# ══════════════════════════════════════════

def detect_multiple_errors(logs):
    """
    Detect error storms.
    Rule: More than 3 ERROR logs from same source
    """
    alerts = []
    error_counts = {}

    for log in logs:
        if log["level"] == "ERROR":
            source = log["source"]
            if source not in error_counts:
                error_counts[source] = {
                    "count":   0,
                    "log_ids": []
                }
            error_counts[source]["count"]   += 1
            error_counts[source]["log_ids"].append(str(log["id"]))

    for source, data in error_counts.items():
        if data["count"] >= 3:
            alert = {
                "rule_name":   "ERROR_STORM_DETECTED",
                "description": (
                    f"Multiple errors detected from source '{source}'. "
                    f"{data['count']} ERROR events detected."
                ),
                "severity":    "MEDIUM",
                "source_ip":   "N/A",
                "log_ids":     ",".join(data["log_ids"]),
                "status":      "NEW"
            }
            alerts.append(alert)
            print(f"[ALERT] Error storm detected in {source} "
                  f"— {data['count']} errors")

    return alerts

# ══════════════════════════════════════════
# RULE 3 — Suspicious Keyword Detection
# ══════════════════════════════════════════

def detect_suspicious_keywords(logs):
    """
    Detect suspicious activity keywords.
    Rule: Log contains known attack keywords
    """
    alerts = []

    SUSPICIOUS_KEYWORDS = [
        "sql injection",
        "xss",
        "cross-site",
        "unauthorized",
        "privilege escalation",
        "root access",
        "sudo",
        "malware",
        "exploit",
        "backdoor",
        "reverse shell",
        "command injection"
    ]

    for log in logs:
        message = log["message"].lower()
        for keyword in SUSPICIOUS_KEYWORDS:
            if keyword in message:
                alert = {
                    "rule_name":   "SUSPICIOUS_KEYWORD",
                    "description": (
                        f"Suspicious keyword '{keyword}' detected "
                        f"in log from '{log['source']}': "
                        f"{log['message'][:100]}"
                    ),
                    "severity":    "CRITICAL",
                    "source_ip":   extract_ip(log["message"]),
                    "log_ids":     str(log["id"]),
                    "status":      "NEW"
                }
                alerts.append(alert)
                print(f"[ALERT] Suspicious keyword '{keyword}' "
                      f"detected in log #{log['id']}")
                break

    return alerts

# ══════════════════════════════════════════
# MAIN RULE ENGINE — Run all rules
# ══════════════════════════════════════════

def run_rule_engine(logs):
    """
    Run all detection rules against logs.
    Returns total number of alerts generated.
    """
    print("\n[ARGUS] Running rule engine...")
    print(f"[ARGUS] Analyzing {len(logs)} logs...\n")

    all_alerts = []

    # Run each rule
    all_alerts += detect_brute_force(logs)
    all_alerts += detect_multiple_errors(logs)
    all_alerts += detect_suspicious_keywords(logs)

    # Save alerts to database
    for alert in all_alerts:
        insert_alert(alert)

    print(f"\n[ARGUS] Rule engine complete.")
    print(f"[ARGUS] {len(all_alerts)} alerts generated.")

    return len(all_alerts)

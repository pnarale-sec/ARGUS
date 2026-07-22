# app/parser/log_parser.py
"""
ARGUS Log Parser
================
Parses raw log lines into structured dictionaries.

Why a dedicated parser module:
- Phase 15 will add parsers for Linux syslog,
  Windows events, Apache, Nginx, etc.
- Each parser lives here, keeping detection
  and storage logic completely separate.
"""

import re
from app.core.logger import setup_logger

logger = setup_logger(__name__)

# Pattern matches our log format:
# 2026-06-20 10:15:32 INFO User admin logged in from 192.168.1.10
LOG_PATTERN = re.compile(
    r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) (\w+) (.+)"
)

def parse_log_line(line: str, source: str) -> dict | None:
    """
    Parse a single log line into a structured dictionary.

    Args:
        line:   Raw log line string
        source: Filename the log came from

    Returns:
        Dictionary with timestamp, level, message, source
        None if line does not match expected format
    """
    match = LOG_PATTERN.match(line)
    if match:
        return {
            "timestamp": match.group(1),
            "level":     match.group(2),
            "message":   match.group(3),
            "source":    source
        }
    logger.debug(f"Could not parse line: {line[:50]}")
    return None
# ingest.py
"""
ARGUS Log Ingestion Script
===========================
Reads log files, parses them, stores in database,
then runs the rule engine to detect threats.

Run this whenever you have new logs to process:
    python ingest.py
"""

import os
from app.database.connection import init_connection_pool, init_db
from app.parser.log_parser import parse_log_line
from app.services.log_service import insert_log, get_all_logs
from app.detection.rule_engine import run_rule_engine
from app.core.logger import setup_logger

logger = setup_logger(__name__)
LOGS_FOLDER = "logs"

def ingest():
    init_connection_pool()
    init_db()

    log_files = os.listdir(LOGS_FOLDER)
    total = 0

    for filename in log_files:
        filepath = os.path.join(LOGS_FOLDER, filename)
        with open(filepath, "r") as file:
            for line in file:
                line = line.strip()
                if line:
                    parsed = parse_log_line(line, filename)
                    if parsed:
                        insert_log(parsed)
                        logger.info(
                            f"Inserted [{parsed['level']}] "
                            f"{parsed['message'][:60]}"
                        )
                        total += 1

    logger.info(f"Ingestion complete — {total} logs inserted")

    all_logs = get_all_logs()
    run_rule_engine(all_logs)

ingest()
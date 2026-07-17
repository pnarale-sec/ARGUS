import os
from log_parser import parse_log_line
from database import init_db, init_alerts_table, insert_log, get_all_logs
from rule_engine import run_rule_engine

LOGS_FOLDER = "logs"

def main():
    # Step 1 - Initialize database tables
    init_db()
    init_alerts_table()
    print("Database initialized.")

    # Step 2 - Read and insert log files
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
                        print(f"Inserted → [{parsed['level']}] "
                              f"{parsed['message']}")
                        total += 1

    print(f"\nDone! {total} logs inserted into database.")

    # Step 3 - Run rule engine on all logs
    all_logs = get_all_logs()
    run_rule_engine(all_logs)

main()
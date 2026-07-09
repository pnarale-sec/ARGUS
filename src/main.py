import os
from log_parser import parse_log_line
from database import init_db, insert_log

LOGS_FOLDER = "logs"

def main():
    # Step 1 - Initialize database
    init_db()
    print("Database initialized.")

    # Step 2 - Read all log files
    log_files = os.listdir(LOGS_FOLDER)

    total = 0

    for filename in log_files:
        filepath = os.path.join(LOGS_FOLDER, filename)

        with open(filepath, "r") as file:
            for line in file:
                line = line.strip()
                if line:
                    # Step 3 - Parse the line
                    parsed = parse_log_line(line, filename)

                    if parsed:
                        # Step 4 - Insert into database
                        insert_log(parsed)
                        print(f"Inserted → [{parsed['level']}] {parsed['message']}")
                        total += 1

    print(f"\nDone! {total} logs inserted into database.")

main()

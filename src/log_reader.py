import os

logs_folder = "logs"

def read_log():

    log_files = os.listdir(logs_folder)

    if not log_files:
        print("log files not found")
        return
    
    for filename in log_files:
        filepath = os.path.join(logs_folder, filename)

        with open(filepath, "r") as file:
            for line in file:
                line = line.strip()  # remove extra spaces and newlines
                if line:  # skip empty lines
                    print(f"[{filename}] {line}")
                    
read_log()

# clear_log.py

import os 

# Defines the path to the application's log file
log_file_path = "app.log" 

if os.path.exists(log_file_path):
    # If the log file exists, open it in write mode to truncate its contents
    with open(log_file_path, 'w') as f:
        f.truncate(0)
    print(f"Content of {log_file_path} cleared successfully.")
else:
    print(f"Log file '{log_file_path}' not found.")
import os
import logging
from datetime import datetime

# Log filename with timestamp
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

# Logs folder path
logs_folder = os.path.join(os.getcwd(), "logs")
os.makedirs(logs_folder, exist_ok=True)  # Create folder if it doesn't exist

# Full path to the log file
LOG_FILE_PATH = os.path.join(logs_folder, LOG_FILE)

# Configure logging
logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# Test logging
logging.info("Logging is set up successfully!")
print(f"Log file created at: {LOG_FILE_PATH}")

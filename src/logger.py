import logging
import os
from datetime import datetime
import sys

# ===== Determine base folder =====
if getattr(sys, "frozen", False):
    # Running as PyInstaller EXE
    BASE_DIR = os.path.dirname(sys.executable)
else:
    # Running as normal Python script
    BASE_DIR = os.path.dirname(__file__)

# ===== Logs folder next to EXE =====
LOG_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)

# ===== Log file with date =====
timestamp = datetime.now().strftime("%Y-%m-%d")
LOG_FILE = os.path.join(LOG_DIR, f"app_log_{timestamp}.log")

# ===== Configure logging =====
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Optional console logging
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
console.setFormatter(formatter)
logging.getLogger().addHandler(console)

# ===== Logging functions =====
def log_info(message):
    logging.info(message)

def log_error(message, exc_info=False, terminate=False):
    """
    Logs an error message.
    exc_info=True logs the full traceback.
    terminate=True stops the program immediately after logging.
    """
    logging.error(message, exc_info=exc_info)
    
    if terminate:
        termination_message = f"Program terminated due to: {message}"
        # Log termination message as ERROR
        logging.error(termination_message)
        # Also print to console
        print(termination_message)
        sys.exit(1)
import logging
import os

# Ensure logs directory exists
LOG_FILE = "tg_messenger.log"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE, encoding='utf-8'),
        logging.StreamHandler()
    ]
)

def log_info(msg):
    """Log an info message"""
    logging.info(msg)

def log_error(msg):
    """Log an error message"""
    logging.error(msg)

def get_logs():
    """Return all logs as a string"""
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r", encoding='utf-8') as f:
            return f.read()
    return ""

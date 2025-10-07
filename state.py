import os
from client import login_state

# ---------------- UPLOAD & DATA PATHS ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
SCHEDULE_FILE = os.path.join(BASE_DIR, "schedule.json")

# Make sure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ---------------- GLOBALS ----------------
# Scheduler status
scheduler_running = False
scheduler_task = None

# Telegram login state (imported from client.py)
# login_state = {"stage": "none", "phone": None, "code_sent": False}

# ---------------- FUNCTION TO RESET LOGIN ----------------
def reset_login_state():
    global login_state
    login_state["stage"] = "none"
    login_state["phone"] = None
    login_state["code_sent"] = False

import os

from dotenv import load_dotenv
load_dotenv()

API_ID = int(os.getenv("API_ID", 0))
API_HASH = os.getenv("API_HASH", "")
SESSION_NAME = "rifat_session"
SCHEDULE_FILE = "schedule.json"
TIMEZONE = "Asia/Dhaka"
PORT = int(os.getenv("PORT", 10000))
UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

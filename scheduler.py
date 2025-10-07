import json
import threading
import time
from datetime import datetime
from state import STATE
from logger import log_info
from croniter import croniter

SCHEDULE_FILE = "schedule.json"

def load_schedule():
    try:
        with open(SCHEDULE_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_schedule(schedule):
    with open(SCHEDULE_FILE, "w") as f:
        json.dump(schedule, f, indent=4)

def should_run(item):
    now = datetime.now()
    if item.get("type") == "date":
        if not item.get("sent") and now.timestamp() >= item["timestamp"]:
            return True
    elif item.get("type") == "cron":
        cron_str = item["cron"]
        last_run = item.get("last_run", 0)
        iter = croniter(cron_str, datetime.fromtimestamp(last_run))
        next_run = iter.get_next(float)
        if now.timestamp() >= next_run:
            return True
    return False

def scheduler_loop(send_func):
    while True:
        if not STATE["scheduler_running"]:
            time.sleep(5)
            continue
        schedule = load_schedule()
        now = datetime.now().timestamp()
        for item in schedule:
            if should_run(item):
                try:
                    send_func(item)
                    if item.get("type") == "date":
                        item["sent"] = True
                    elif item.get("type") == "cron":
                        item["last_run"] = now
                    save_schedule(schedule)
                except Exception as e:
                    log_info(f"Failed to send: {e}")
        time.sleep(5)

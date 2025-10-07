from datetime import datetime

LOG_HISTORY = []

def add_log(msg: str):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    LOG_HISTORY.append(f"[{now}] {msg}")
    if len(LOG_HISTORY) > 300:
        LOG_HISTORY.pop(0)
    print(msg)

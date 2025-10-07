import threading

LOG_HISTORY = []
lock = threading.Lock()

def add_log(message):
    with lock:
        LOG_HISTORY.append(message)
        print(message)

def get_logs():
    with lock:
        return LOG_HISTORY[-100:]  # last 100 logs

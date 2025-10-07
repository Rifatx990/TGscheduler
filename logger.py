import threading
logs = []

def add_log(message):
    logs.append(message)
    print(message)

def get_logs():
    return logs[-100:]  # last 100 logs

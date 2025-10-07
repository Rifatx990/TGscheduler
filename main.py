import asyncio
import threading
from flask import Flask
from logger import add_log
from config import PORT

from routes.dashboard import bp_dashboard
from routes.login_route import bp_login

app = Flask(__name__)
app.register_blueprint(bp_dashboard)
app.register_blueprint(bp_login)

scheduler_running = False
scheduler_task = None

def start_scheduler(async_func):
    global scheduler_running, scheduler_task
    if scheduler_running:
        add_log("⚠️ Scheduler already running.")
        return

    scheduler_running = True

    def run_loop():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(async_func())
        finally:
            loop.close()
            add_log("🛑 Scheduler event loop closed.")
            global scheduler_running
            scheduler_running = False

    scheduler_task = threading.Thread(target=run_loop, daemon=True)
    scheduler_task.start()
    add_log("✅ Scheduler thread started.")

def stop_scheduler():
    global scheduler_running
    if scheduler_running:
        scheduler_running = False
        add_log("🛑 Stop signal sent to scheduler.")

if __name__ == "__main__":
    add_log("🌐 Dashboard ready. Telegram login required.")
    app.run(host="0.0.0.0", port=PORT, threaded=True)

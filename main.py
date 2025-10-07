import asyncio
import threading
from flask import Flask
from logger import add_log
from config import PORT

# ---------------- IMPORT BLUEPRINTS ----------------
from routes.dashboard import bp_dashboard
from routes.schedule_api import bp_schedule
from routes.logs import bp_logs
from routes.login_route import bp_login
from routes.send_now import bp_send_now

# ---------------- FLASK APP ----------------
app = Flask(__name__)

# Register all blueprints
app.register_blueprint(bp_dashboard)
app.register_blueprint(bp_schedule)
app.register_blueprint(bp_logs)
app.register_blueprint(bp_login)
app.register_blueprint(bp_send_now)

# ---------------- GLOBALS ----------------
scheduler_running = False
scheduler_task = None

# ---------------- SCHEDULER FUNCTIONS ----------------
def start_scheduler(async_func):
    """Start the async scheduler in a separate thread."""
    global scheduler_running, scheduler_task
    if scheduler_running:
        add_log("⚠️ Scheduler already running.")
        return

    scheduler_running = True

    def run_loop():
        """Run async scheduler inside a new event loop."""
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
    """Stop the running scheduler."""
    global scheduler_running
    if scheduler_running:
        scheduler_running = False
        add_log("🛑 Stop signal sent to scheduler.")
    else:
        add_log("⚠️ Scheduler is not running.")

# ---------------- MAIN ----------------
if __name__ == "__main__":
    add_log("🌐 Dashboard ready. Telegram login required.")
    # threaded=True allows Flask to handle requests while async scheduler runs
    app.run(host="0.0.0.0", port=PORT, threaded=True)

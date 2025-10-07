import asyncio
from flask import Flask
from routes.dashboard import bp_dashboard
from routes.schedule_api import bp_schedule
from routes.logs import bp_logs
from routes.login_route import bp_login
from routes.send_now import bp_send_now
from logger import add_log
from config import PORT

# ---------------- FLASK APP ----------------
app = Flask(__name__)
app.register_blueprint(bp_dashboard)
app.register_blueprint(bp_schedule)
app.register_blueprint(bp_logs)
app.register_blueprint(bp_login)
app.register_blueprint(bp_send_now)

# ---------------- GLOBALS ----------------
# To hold scheduler status
scheduler_running = False
scheduler_task = None

# ---------------- FUNCTIONS ----------------
def start_scheduler(async_func):
    global scheduler_running, scheduler_task
    if scheduler_running:
        add_log("⚠️ Scheduler already running.")
        return
    scheduler_running = True

    def run_loop():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(async_func())

    import threading
    t = threading.Thread(target=run_loop, daemon=True)
    t.start()
    add_log("✅ Scheduler thread started.")

def stop_scheduler():
    global scheduler_running
    scheduler_running = False
    add_log("🛑 Stop signal sent.")

# ---------------- MAIN ----------------
if __name__ == "__main__":
    add_log("🌐 Dashboard ready. Telegram login required.")
    # Use threaded=True to allow Flask to handle multiple requests while async scheduler runs
    app.run(host="0.0.0.0", port=PORT, threaded=True)

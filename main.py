import threading
import asyncio
from flask import Flask
from routes import bp_routes
from config import API_ID, API_HASH, SESSION_NAME
from scheduler import scheduler_loop
from state import STATE
from logger import log_info
import os

# ---------------- Flask App ----------------
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './uploads'

# Ensure uploads folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Register all blueprints from bp_routes
for bp in bp_routes:
    app.register_blueprint(bp)

# ---------------- Telegram Client ----------------
client = None  # global Telegram client

def start_client():
    """Initialize and start Telegram client in a thread"""
    global client
    # Create a new event loop for this thread
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    # Initialize client
    client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

    async def init_client():
        await client.start()  # await coroutine
        log_info("Telegram Client Started")

    # Run coroutine in the loop
    loop.run_until_complete(init_client())

# Start Telegram client in a background thread
threading.Thread(target=start_client, daemon=True).start()

# ---------------- Scheduler ----------------
def send_func(item):
    """Function called by scheduler to send messages"""
    global client
    if client is None:
        log_info("Telegram client not ready yet")
        return

    # Import dynamically to avoid circular imports
    from routes.send_now import send_message

    import asyncio
    # Run async send in a temporary event loop
    try:
        asyncio.run(send_message(client, item))
    except Exception as e:
        log_info(f"Scheduler send error: {e}")

# Start scheduler loop in a background thread
threading.Thread(target=scheduler_loop, args=(send_func,), daemon=True).start()

# ---------------- Run Flask ----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

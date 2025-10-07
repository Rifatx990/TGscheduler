from flask import Flask
from routes import bp_routes  # bp_routes is a list
from config import API_ID, API_HASH, SESSION_NAME
from telethon import TelegramClient
from scheduler import scheduler_loop
from state import STATE
from logger import log_info
import threading
import asyncio

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './uploads'

# Register all blueprints
for bp in bp_routes:
    app.register_blueprint(bp)

# Global Telegram client
client = None

def start_client():
    global client
    # Create a new event loop for this thread
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    # Initialize Telegram client
    client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
    
    # Start the client
    loop.run_until_complete(client.start())
    log_info("Telegram Client Started")

# Start Telegram client in background thread
threading.Thread(target=start_client, daemon=True).start()

# Scheduler function
def send_func(item):
    global client
    if client is None:
        log_info("Telegram client not ready yet")
        return
    # Import send_message dynamically to avoid circular import
    from routes.send_now import send_message
    import asyncio
    # Run send_message in a temporary event loop
    asyncio.run(send_message(client, item))

# Start scheduler in background thread
threading.Thread(target=scheduler_loop, args=(send_func,), daemon=True).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

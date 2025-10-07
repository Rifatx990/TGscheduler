from flask import Flask
from routes import bp_routes  # bp_routes is now a list
from config import API_ID, API_HASH, SESSION_NAME
from telethon import TelegramClient
from scheduler import scheduler_loop
from state import STATE
from logger import log_info
import threading, asyncio

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './uploads'

# Register all blueprints in bp_routes list
for bp in bp_routes:
    app.register_blueprint(bp)

# Initialize Telegram client
client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

def start_client():
    async def run():
        await client.start()
        log_info("Telegram Client Started")
    asyncio.run(run())

# Start Telegram client in background thread
threading.Thread(target=start_client, daemon=True).start()

# Scheduler function to send messages
def send_func(item):
    from routes.send_now import send_message
    send_message(client, item)

# Start scheduler loop in background thread
threading.Thread(target=scheduler_loop, args=(send_func,), daemon=True).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

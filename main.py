from flask import Flask
from routes import bp_routes
from config import API_ID, API_HASH, SESSION_NAME
from telethon import TelegramClient
from scheduler import scheduler_loop
from state import STATE
from logger import log_info
import threading
import asyncio

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './uploads'
app.register_blueprint(bp_routes)

client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

def start_client():
    async def run():
        await client.start()
        log_info("Telegram Client Started")
    asyncio.run(run())

# Start Telegram client in background
threading.Thread(target=start_client).start()

# Start scheduler in background
def send_func(item):
    from routes.send_now import send_message
    send_message(client, item)

threading.Thread(target=scheduler_loop, args=(send_func,), daemon=True).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

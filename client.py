import asyncio
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError, PhoneCodeInvalidError
from config import API_ID, API_HASH, SESSION_NAME
from logger import add_log

client = None
login_state = {"stage": "none", "phone": None, "code_sent": False}

async def ensure_client():
    global client
    if client is None:
        client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
        await client.connect()
    elif not client.is_connected():
        await client.connect()
    return client

async def send_message(to, message, file_path=None):
    c = await ensure_client()
    try:
        if file_path:
            await c.send_file(to, file_path, caption=message)
        else:
            await c.send_message(to, message)
        add_log(f"✅ Sent to {to}: {message} {'with file '+file_path if file_path else ''}")
    except Exception as e:
        add_log(f"❌ Failed to send to {to}: {e}")

async def login_step(phone=None, code=None, password=None):
    global client, login_state
    c = await ensure_client()
    try:
        if login_state["stage"] == "none" and phone:
            await c.send_code_request(phone)
            login_state = {"stage": "code", "phone": phone, "code_sent": True}
            add_log(f"📩 Code sent to {phone}")
            return "Code sent, please enter it."
        elif login_state["stage"] == "code" and code:
            try:
                await c.sign_in(login_state["phone"], code)
            except SessionPasswordNeededError:
                login_state["stage"] = "password"
                add_log("🔒 Two-factor password required.")
                return "2FA required. Enter password."
            login_state["stage"] = "none"
            add_log("✅ Logged in successfully!")
            return "Logged in successfully!"
        elif login_state["stage"] == "password" and password:
            await c.sign_in(login_state["phone"], password=password)
            login_state["stage"] = "none"
            add_log("✅ Logged in with 2FA successfully!")
            return "Logged in successfully with 2FA!"
        return "No action performed."
    except PhoneCodeInvalidError:
        add_log("❌ Invalid code.")
        return "Invalid code. Retry."
    except Exception as e:
        add_log(f"❌ Login error: {e}")
        return f"Login error: {e}"

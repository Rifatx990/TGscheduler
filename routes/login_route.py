from flask import Blueprint, request, redirect, url_for
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError, PhoneCodeInvalidError
from config import API_ID, API_HASH
from logger import add_log
import threading

bp_login = Blueprint("login_route", __name__)

client = TelegramClient("rifat_session", API_ID, API_HASH)
login_state = {"stage":"none","phone":None,"code_sent":False,"2fa":False}

def async_login(phone=None, code=None, password=None):
    import asyncio

    async def login_task():
        global client, login_state
        await client.connect()
        try:
            if login_state["stage"] == "none" and phone:
                await client.send_code_request(phone)
                login_state["stage"] = "code"
                login_state["phone"] = phone
                login_state["code_sent"] = True
                add_log(f"📩 Code sent to {phone}")
            elif login_state["stage"] == "code" and code:
                try:
                    await client.sign_in(login_state["phone"], code)
                except SessionPasswordNeededError:
                    login_state["stage"] = "password"
                    login_state["2fa"] = True
                    add_log("🔒 2FA password required")
                else:
                    login_state["stage"] = "none"
                    add_log("✅ Logged in successfully!")
            elif login_state["stage"] == "password" and password:
                await client.sign_in(login_state["phone"], password=password)
                login_state["stage"] = "none"
                login_state["2fa"] = False
                add_log("✅ Logged in with 2FA successfully!")
        except PhoneCodeInvalidError:
            add_log("❌ Invalid code")
        except Exception as e:
            add_log(f"❌ Login error: {e}")

    threading.Thread(target=lambda: asyncio.run(login_task()), daemon=True).start()

@bp_login.route("/login", methods=["POST"])
def login_route():
    phone = request.form.get("phone")
    code = request.form.get("code")
    password = request.form.get("password")

    if phone:
        async_login(phone=phone)
    elif code:
        async_login(code=code)
    elif password:
        async_login(password=password)

    # Redirect to dashboard to show proper form
    return redirect(url_for("dashboard.dashboard"))

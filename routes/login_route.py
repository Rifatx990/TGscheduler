from flask import Blueprint, request, render_template, redirect, url_for
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError, PhoneCodeInvalidError
from config import API_ID, API_HASH, SESSION_NAME
from logger import add_log
import threading
import asyncio

bp_login = Blueprint("login_route", __name__)

login_state = {"stage":"none","phone":None,"code_sent":False,"2fa":False}
client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

def async_login(phone=None, code=None, password=None):
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

    # Render dashboard again showing proper form based on stage
    from routes.dashboard import HTML_DASHBOARD
    login_required = login_state["stage"] != "none"
    return render_template_string(HTML_DASHBOARD,
                                  login_required=login_required,
                                  login_state=login_state,
                                  data="[]")

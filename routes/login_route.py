from flask import Blueprint, request, jsonify
from client import login_step
from state import login_state
from logger import add_log
import asyncio

bp_login = Blueprint("login", __name__)

# Use a single global event loop for all async tasks
loop = asyncio.get_event_loop()

@bp_login.route("/login", methods=["POST"])
def login_route():
    data = request.json or request.form  # Supports both JSON and form POST
    phone = data.get("phone")
    code = data.get("code")
    password = data.get("password")

    async def login_async():
        return await login_step(phone=phone, code=code, password=password)

    try:
        # Schedule coroutine safely on the global loop
        future = asyncio.run_coroutine_threadsafe(login_async(), loop)
        result = future.result(timeout=30)  # Increased timeout for slow Telegram responses
        add_log(f"ℹ️ Login attempt result: {result}")
        return jsonify({"status": "ok", "message": result, "stage": login_state["stage"]})
    except asyncio.TimeoutError:
        add_log("❌ Login timeout. Try again.")
        return jsonify({"status": "error", "message": "Login timeout. Try again."})
    except Exception as e:
        add_log(f"❌ Login route error: {e}")
        return jsonify({"status": "error", "message": f"Login error: {e}"})

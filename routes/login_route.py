from flask import Blueprint, request, jsonify
from client import login_step, login_state
import asyncio
from logger import add_log

bp_login = Blueprint("login", __name__)
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

@bp_login.route("/login", methods=["POST"])
def login_route():
    phone = request.form.get("phone")
    code = request.form.get("code")
    password = request.form.get("password")

    async def login_async():
        return await login_step(phone=phone, code=code, password=password)

    try:
        future = asyncio.run_coroutine_threadsafe(login_async(), loop)
        result = future.result(timeout=30)
        add_log(f"ℹ️ Login attempt result: {result}")
        return jsonify({"status": "ok", "message": result, "stage": login_state["stage"]})
    except asyncio.TimeoutError:
        add_log("❌ Login timeout. Try again.")
        return jsonify({"status": "error", "message": "Login timeout. Try again."})
    except Exception as e:
        add_log(f"❌ Login route error: {e}")
        return jsonify({"status": "error", "message": f"Login error: {e}"})

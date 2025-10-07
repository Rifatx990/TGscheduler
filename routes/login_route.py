from flask import Blueprint, request, jsonify
from client import login_step
import asyncio
from logger import add_log

bp_login = Blueprint("login", __name__)
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

@bp_login.route("/login", methods=["POST"])
def login_route():
    data = request.json
    phone = data.get("phone")
    code = data.get("code")
    password = data.get("password")

    async def login_async():
        return await login_step(phone=phone, code=code, password=password)

    try:
        future = asyncio.run_coroutine_threadsafe(login_async(), loop)
        result = future.result(timeout=20)
        return jsonify({"status": "ok", "message": result})
    except asyncio.TimeoutError:
        add_log("❌ Login timeout. Try again.")
        return jsonify({"status": "error", "message": "Login timeout. Try again."})
    except Exception as e:
        add_log(f"❌ Login route error: {e}")
        return jsonify({"status": "error", "message": f"Login error: {e}"})

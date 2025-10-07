from flask import Blueprint, request, jsonify
from telethon.errors import SessionPasswordNeededError
from telethon.sync import TelegramClient
from config import API_ID, API_HASH, SESSION_NAME
from state import STATE
from logger import log_info

bp_login = Blueprint("login_route", __name__)

client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

@bp_login.route("/login", methods=["POST"])
def login():
    data = request.json
    phone = data.get("phone")
    code = data.get("code")
    try:
        client.start(phone=phone, code_callback=lambda: code)
        STATE["is_logged_in"] = True
        log_info(f"Logged in as {phone}")
        return jsonify({"status":"success"})
    except SessionPasswordNeededError:
        STATE["pending_2fa"] = True
        return jsonify({"status":"2fa_required"})
    except Exception as e:
        log_info(str(e))
        return jsonify({"status":"error", "msg":str(e)})

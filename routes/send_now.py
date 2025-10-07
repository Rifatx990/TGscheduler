from flask import request, Blueprint, jsonify
from logger import log_info
import os
import asyncio

bp_send = Blueprint("send_now", __name__)

async def send_message_async(client, item):
    """Async function to send message or file"""
    target = item.get("user")  # username or chat id
    message = item.get("message")
    file_path = item.get("file")

    if file_path:
        await client.send_file(target, file_path, caption=message)
    else:
        await client.send_message(target, message)

def send_message(client, item):
    """Wrapper to run async send_message_async"""
    if client is None:
        log_info("Telegram client not ready yet")
        return
    asyncio.run(send_message_async(client, item))

@bp_send.route("/send_now", methods=["POST"])
def send_now_route():
    from main import client  # import dynamically to avoid circular import
    try:
        if request.content_type.startswith('multipart/form-data'):
            user = request.form.get("user")
            message = request.form.get("message")
            file = request.files.get("file")
            file_path = None
            if file:
                # ensure uploads folder exists
                os.makedirs("./uploads", exist_ok=True)
                file_path = os.path.join("./uploads", file.filename)
                file.save(file_path)
            item = {"user": user, "message": message, "file": file_path}
        else:
            item = request.json

        # Send message asynchronously
        send_message(client, item)

        return jsonify({"status":"success"})
    except Exception as e:
        log_info(str(e))
        return jsonify({"status":"error", "msg": str(e)})

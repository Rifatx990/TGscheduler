from flask import request, Blueprint, jsonify
from logger import log_info
import os

bp_send = Blueprint("send_now", __name__)

def send_message(client, item):
    target = item.get("user")  # username or chat id
    message = item.get("message")
    file_path = item.get("file")

    if file_path:
        client.send_file(target, file_path, caption=message)
    else:
        client.send_message(target, message)

@bp_send.route("/send_now", methods=["POST"])
def send_now_route():
    from main import client
    if request.content_type.startswith('multipart/form-data'):
        user = request.form.get("user")
        message = request.form.get("message")
        file = request.files.get("file")
        file_path = None
        if file:
            file_path = os.path.join("./uploads", file.filename)
            file.save(file_path)
        item = {"user": user, "message": message, "file": file_path}
    else:
        item = request.json
    try:
        send_message(client, item)
        return jsonify({"status":"success"})
    except Exception as e:
        log_info(str(e))
        return jsonify({"status":"error", "msg": str(e)})

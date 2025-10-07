from flask import Blueprint, request
from client import send_message
from werkzeug.utils import secure_filename
from config import UPLOAD_FOLDER
import os
import asyncio

bp_send_now = Blueprint("send_now", __name__)

@bp_send_now.route("/send_now", methods=["POST"])
def send_now():
    to = request.form.get("to")
    message = request.form.get("message")
    file = request.files.get("file")
    file_path = None
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)
    # Run async send
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(send_message(to, message, file_path))
    return "✅ Message sent!"

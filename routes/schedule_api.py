from flask import Blueprint, request, jsonify
from scheduler import start_scheduler, stop_scheduler, load_schedules
from config import UPLOAD_FOLDER, SCHEDULE_FILE
from logger import add_log
from werkzeug.utils import secure_filename
import json
import os

bp_schedule = Blueprint("schedule_api", __name__)

@bp_schedule.route("/start", methods=["POST"])
def start_route():
    start_scheduler()
    return jsonify({"status":"started"})

@bp_schedule.route("/stop", methods=["POST"])
def stop_route():
    stop_scheduler()
    return jsonify({"status":"stopped"})

@bp_schedule.route("/reload", methods=["POST"])
def reload_route():
    add_log("🔁 Reloaded schedule.")
    load_schedules()
    return jsonify({"status":"reloaded"})

@bp_schedule.route("/update", methods=["POST"])
def update_schedule():
    try:
        data = json.loads(request.form["data"])
        files = request.files.getlist("files")
        for i, file in enumerate(files):
            if i < len(data):
                filename = secure_filename(file.filename)
                file.save(os.path.join(UPLOAD_FOLDER, filename))
                data[i]["file"] = filename
        with open(SCHEDULE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        add_log("💾 schedule.json updated successfully.")
        return "✅ Saved successfully!"
    except Exception as e:
        add_log(f"❌ Save failed: {e}")
        return f"❌ {e}"

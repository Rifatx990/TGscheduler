from flask import Blueprint, request, jsonify
from scheduler import load_schedule, save_schedule
from state import STATE
import os
import time

bp_scheduler = Blueprint("scheduler_api", __name__)

@bp_scheduler.route("/scheduler", methods=["GET"])
def get_schedule():
    return jsonify(load_schedule())

@bp_scheduler.route("/scheduler", methods=["POST"])
def add_schedule():
    data = request.form if request.content_type.startswith('multipart/form-data') else request.json
    schedule = load_schedule()
    sched_type = data.get("type", "date")  # 'date' or 'cron'
    item = {
        "type": sched_type,
        "user": data.get("user"),
        "message": data.get("message"),
        "file": None,
        "sent": False,
        "last_run": 0
    }

    # Handle file upload
    if request.files:
        f = request.files["file"]
        f.save(os.path.join("./uploads", f.filename))
        item["file"] = f.filename

    # Date type
    if sched_type == "date":
        item["timestamp"] = int(data.get("timestamp"))
    elif sched_type == "cron":
        item["cron"] = data.get("cron")  # e.g., "0 10 * * *" for daily 10:00

    schedule.append(item)
    save_schedule(schedule)
    return jsonify({"status":"success"})

@bp_scheduler.route("/scheduler/start", methods=["POST"])
def start_scheduler():
    STATE["scheduler_running"] = True
    return jsonify({"status":"started"})

@bp_scheduler.route("/scheduler/stop", methods=["POST"])
def stop_scheduler():
    STATE["scheduler_running"] = False
    return jsonify({"status":"stopped"})

@bp_scheduler.route("/scheduler/delete/<int:index>", methods=["DELETE"])
def delete_schedule(index):
    schedule = load_schedule()
    if 0 <= index < len(schedule):
        schedule.pop(index)
        save_schedule(schedule)
        return jsonify({"status":"deleted"})
    return jsonify({"status":"error","msg":"Invalid index"})

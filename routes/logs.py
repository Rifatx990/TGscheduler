from flask import Blueprint, jsonify
from logger import get_logs

bp_logs = Blueprint("logs", __name__)

@bp_logs.route("/logs")
def logs_route():
    return jsonify({"logs": get_logs()})

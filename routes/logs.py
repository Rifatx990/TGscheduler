from flask import Blueprint, jsonify
from logger import LOG_HISTORY

bp_logs = Blueprint("logs", __name__)

@bp_logs.route("/logs")
def logs_route():
    return jsonify({"logs": LOG_HISTORY})

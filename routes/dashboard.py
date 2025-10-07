from flask import Blueprint, render_template
from client import login_state
from config import SCHEDULE_FILE
import os

bp_dashboard = Blueprint("dashboard", __name__)

@bp_dashboard.route("/")
def dashboard():
    login_required = not os.path.exists("rifat_session.session")
    data = ""
    if os.path.exists(SCHEDULE_FILE):
        with open(SCHEDULE_FILE,"r",encoding="utf-8") as f:
            data = f.read()
    return render_template("dashboard.html", login_required=login_required, login_state=login_state, data=data)

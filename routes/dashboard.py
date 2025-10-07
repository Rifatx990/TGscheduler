from flask import Blueprint, render_template

bp_dashboard = Blueprint("dashboard", __name__, template_folder="../templates")

@bp_dashboard.route("/")
def dashboard():
    return render_template("dashboard.html")

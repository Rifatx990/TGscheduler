from flask import Blueprint, render_template_string, request
from logger import add_log

bp_dashboard = Blueprint("dashboard", __name__)

# Global login state
login_state = {"stage": "none", "phone": None, "code_sent": False, "2fa": False}

HTML_DASHBOARD = """
<!DOCTYPE html>
<html>
<head>
<title>Telegram Scheduler</title>
</head>
<body>
<h2>Telegram Scheduler Dashboard</h2>

{% if login_required %}
<form method="POST" action="/login">
  {% if login_state.stage == 'none' %}
    <label>Phone number (+8801xxxxxx):</label>
    <input type="text" name="phone" required>
    <button type="submit">Send Code</button>
  {% elif login_state.stage == 'code' %}
    <label>Code sent to {{ login_state.phone }}:</label>
    <input type="text" name="code" required>
    <button type="submit">Login</button>
  {% elif login_state.stage == 'password' %}
    <label>2FA Password:</label>
    <input type="password" name="password" required>
    <button type="submit">Login</button>
  {% endif %}
</form>
{% else %}
<p>✅ Logged in! Scheduler & send messages available.</p>
{% endif %}
</body>
</html>
"""

@bp_dashboard.route("/", methods=["GET"])
def dashboard():
    login_required = login_state["stage"] != "none"
    return render_template_string(
        HTML_DASHBOARD,
        login_required=login_required,
        login_state=login_state
    )

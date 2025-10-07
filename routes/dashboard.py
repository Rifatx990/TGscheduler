from flask import Blueprint, render_template_string, request
import os
from state import SCHEDULE_FILE, UPLOAD_FOLDER
from logger import get_logs
from routes.login_route import login_state

bp_dashboard = Blueprint("dashboard", __name__)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

HTML_DASHBOARD = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Telegram Scheduler Dashboard</title>
<style>
body{font-family:sans-serif;padding:20px;color:#333;}
h2{text-align:center;}
textarea{width:100%;height:200px;font-family:monospace;border-radius:8px;padding:10px;border:1px solid #ccc;}
button{padding:10px 15px;margin:5px;cursor:pointer;border-radius:6px;border:none;background:#007bff;color:white;}
pre{background:#000;color:#0f0;padding:10px;height:200px;overflow-y:scroll;border-radius:8px;}
input[type="text"], input[type="password"]{width:100%;padding:8px;margin:5px 0;border-radius:6px;border:1px solid #ccc;}
</style>
<script>
async function reloadLogs(){
    const res=await fetch('/logs');
    const data=await res.json();
    document.getElementById('logs').innerText=data.logs.join("\\n");
}
setInterval(reloadLogs,3000);
</script>
</head>
<body>
<h2>📅 Telegram Scheduler Dashboard</h2>

{% if login_state.stage != 'none' %}
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

<h3>📜 Live Logs</h3>
<pre id="logs">Loading logs...</pre>
</body>
</html>
"""

@bp_dashboard.route("/", methods=["GET"])
def dashboard():
    if os.path.exists(SCHEDULE_FILE):
        with open(SCHEDULE_FILE, "r", encoding="utf-8") as f:
            data = f.read()
    else:
        data = "[]"
    return render_template_string(HTML_DASHBOARD,
                                  login_state=login_state,
                                  data=data)

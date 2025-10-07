from flask import Blueprint, render_template_string
import os
from logger import add_log

bp_dashboard = Blueprint("dashboard", __name__)

SCHEDULE_FILE = "schedule.json"
UPLOAD_FOLDER = "uploads"
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
async function reloadLogs(){const res=await fetch('/logs');const data=await res.json();document.getElementById('logs').innerText=data.logs.join("\\n");}
setInterval(reloadLogs,3000);

async function startScheduler(){await fetch('/start',{method:'POST'});reloadLogs();}
async function stopScheduler(){await fetch('/stop',{method:'POST'});reloadLogs();}
async function reloadScheduler(){await fetch('/reload',{method:'POST'});reloadLogs();}
</script>
</head>
<body>
<h2>📅 Telegram Scheduler Dashboard</h2>

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
<form method="POST" action="/update" enctype="multipart/form-data">
<h3>📝 Edit schedule.json & Upload Files</h3>
<textarea name="data">{{ data }}</textarea><br>
<label>Upload files (per task):</label>
<input type="file" name="files" multiple><br>
<button type="submit">💾 Save Schedule</button>
</form>

<h3>⚙️ Controls</h3>
<button onclick="startScheduler()">▶️ Start Scheduler</button>
<button onclick="stopScheduler()">⏹ Stop Scheduler</button>
<button onclick="reloadScheduler()">🔁 Reload Schedule</button>

<h3>📜 Live Logs</h3>
<pre id="logs">Loading logs...</pre>
{% endif %}
</body>
</html>
"""

@bp_dashboard.route("/")
def dashboard():
    # Import login_state from login_route
    from routes.login_route import login_state
    login_required = login_state["stage"] != "none"

    # Load schedule.json for display
    if os.path.exists(SCHEDULE_FILE):
        with open(SCHEDULE_FILE, "r", encoding="utf-8") as f:
            data = f.read()
    else:
        data = "[]"

    return render_template_string(HTML_DASHBOARD,
                                  login_required=login_required,
                                  login_state=login_state,
                                  data=data)

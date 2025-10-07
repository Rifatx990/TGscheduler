from flask import Flask
from routes.dashboard import bp_dashboard
from routes.schedule_api import bp_schedule
from routes.logs import bp_logs
from routes.login_route import bp_login
from logger import add_log
from config import PORT

app = Flask(__name__)
app.register_blueprint(bp_dashboard)
app.register_blueprint(bp_schedule)
app.register_blueprint(bp_logs)
app.register_blueprint(bp_login)

if __name__=="__main__":
    add_log("🌐 Dashboard ready. Telegram login required.")
    app.run(host="0.0.0.0", port=PORT)

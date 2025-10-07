from .dashboard import bp_dashboard
from .login_route import bp_login
from .logs import bp_logs
from .scheduler_api import bp_scheduler
from .send_now import bp_send

# Combine all blueprints in a list
bp_routes = [bp_dashboard, bp_login, bp_logs, bp_scheduler, bp_send]

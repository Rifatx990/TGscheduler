from .dashboard import bp_dashboard
from .logs import bp_logs
from .scheduler_api import bp_scheduler
from .send_now import bp_send

# Combine all static blueprints in a list
bp_routes = [bp_dashboard, bp_logs, bp_scheduler, bp_send]

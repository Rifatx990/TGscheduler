from flask import Blueprint

bp_routes = Blueprint('routes', __name__)

from . import dashboard, login_route, logs, scheduler_api, send_now

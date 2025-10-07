from flask import Blueprint, request
from client import login_step
import asyncio

bp_login = Blueprint("login_route", __name__)

@bp_login.route("/login", methods=["POST"])
def login_route():
    phone = request.form.get("phone")
    code = request.form.get("code")
    password = request.form.get("password")
    result = asyncio.run(login_step(phone=phone, code=code, password=password))
    return result

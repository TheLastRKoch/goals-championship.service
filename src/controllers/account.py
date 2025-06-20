from flask_session import Session
from os import environ as env

from flask import Blueprint, render_template, request, redirect, session
from flask.views import MethodView

from services.todoist import ServiceTodoist
from services.notion import ServiceNotion


class AccountController:
    bp = Blueprint("account", __name__, url_prefix="/account")

    @bp.route("/login", methods=["GET"])
    def render_login_page():
        return render_template("login.html")

    @bp.route("/login", methods=["POST"])
    def login():
        # Init services
        todoist = ServiceTodoist()
        notion = ServiceNotion()

        session["source"] = request.form["source"]
        token = request.form["token"]
        auth_status = False

        if session["source"] == "Todoist":
            auth_status = todoist.check_token_auth(token)
        elif session["source"] == "Notion":
            auth_status = notion.check_token_auth(token)

        if auth_status:
            session["token"] = token
            return redirect("/")
        return {"msg": "Error the token is invalid"}

    @bp.route("/logout", methods=["get"])
    def logout():
        session.clear()
        return redirect("/")

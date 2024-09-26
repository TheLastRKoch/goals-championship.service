from flask import render_template, request, redirect, session
from flask.views import MethodView
from flask_session import Session
from os import environ as env

from services.todoist import ServiceTodoist
from services.notion import ServiceNotion


class LoginController(MethodView):
    def get(self):
        return render_template("login.html")

    def post(self):
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
        return {
            "msg": "Error the token is invalid"
        }


class LogoutController(MethodView):
    def get(self):
        session.clear()
        return redirect("/")

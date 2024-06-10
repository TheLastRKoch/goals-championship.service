from flask import render_template, request, redirect, session
from services.todoist import ServiceTodoist
from flask.views import MethodView
from flask_session import Session
from os import environ as env


class LoginController(MethodView):
    def get(self):
        return render_template("login.html")

    def post(self):
        # Init services
        todoist = ServiceTodoist()

        token = request.form["token"]
        if todoist.check_token_auth(token):
            session["token"] = token
            return redirect("/")
        return {
            "msg":"Error the token is invalid"
        }
    
class LogoutController(MethodView):
    def get(self):
        session.clear()
        return redirect("/")
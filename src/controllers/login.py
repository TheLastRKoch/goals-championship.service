from flask import render_template, request, redirect
from flask.views import MethodView
from os import environ as env

class LoginController(MethodView):
    def get(self):
        return render_template("login.jinja2")

    def post(self):
        token = request.form["token"]
        #TODO: Check if token is valid if not show an error
        return {"msg":"Login successfully"}
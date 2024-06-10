from flask.views import MethodView
from flask import render_template, redirect, session


class IndexController(MethodView):
    def get(self):
        if "token" in session.keys():
            return redirect("goals")
        return redirect("account/login")
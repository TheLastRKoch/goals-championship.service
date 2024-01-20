from flask import render_template, request, session, redirect, url_for
from flask.views import MethodView


class LoginController(MethodView):
    def get(self):
        return render_template("login.html")

    def post(self):
        session["token"] = request.form["token"]
        # Save the token to session for 30 mins
        return redirect('/goals')

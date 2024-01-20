from flask import render_template, session, redirect
from flask.views import MethodView


class GoalController(MethodView):
    def get(self):
        return render_template("goal_request.html")

    def post(self):
        view = session["token"]
        return redirect("/goal/list")


class GoalListController(MethodView):
    def get(self):
        return render_template("goal_list.html")

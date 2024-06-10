from flask import render_template, session, redirect, request, session, Response
from flask.views import MethodView

from services.formatter import ServiceFormatter
from services.todoist import ServiceTodoist
from utils.files import UtilFile


class GoalController(MethodView):
    def get(self):
        if "token" not in session.keys():
            return render_template("index.html")
        return render_template("filter_goals.html")

    def post(self):
        session["filter_date"] = request.form["filterDate"]
        return redirect("goal/list")


class GoalListController(MethodView):
    def get(self):
        if "token" not in session.keys():
            return render_template("index.html")

        # Init service
        todoist = ServiceTodoist()
        formatter = ServiceFormatter()

        token = session["token"]
        filter_date = session["filter_date"]

        task_list = todoist.get_task_list(token, filter_date)
        project_list = todoist.get_project_list(token)
        task_list = formatter.merge_tasks_projects(task_list, project_list)

        return render_template("goal_list.html", task_list=task_list)


class DownloadGoalList(MethodView):
    def get(self):
        # Init services
        todoist = ServiceTodoist()
        formatter = ServiceFormatter()

        # Init utils
        files = UtilFile()

        token = session["token"]
        filter_date = session["filter_date"]

        task_list = todoist.get_task_list(token, filter_date)
        project_list = todoist.get_project_list(token)
        task_list = formatter.merge_tasks_projects(task_list, project_list)

        csv_data = files.json_to_csv(task_list)

        return Response(
            csv_data,
            mimetype="text/csv",
            headers={"Content-Disposition": "attachment;filename=Goals.csv"}
        )

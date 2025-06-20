from flask import Blueprint, render_template, session, redirect, request, Response
from services.formatter import ServiceFormatter
from services.todoist import ServiceTodoist
from services.notion import ServiceNotion
from utils.files import UtilFile
from utils.dates import UtilsDate
from os import environ as env


class GoalController:
    bp = Blueprint("goal", __name__, url_prefix="/goal")

    @bp.route("/", methods=["GET"])
    def home():
        # TODO: Redirect to /project/filter only for Zenkit
        return redirect("/goal/filter")

    @bp.route("/filter", methods=["GET"])
    def render_goal_filter():
        if "token" not in session:
            return render_template("index.html")
        return render_template("goal_filter.html")

    @bp.route("/filter", methods=["POST"])
    def goal_filter():
        session["filter_date"] = request.form["filterDate"]
        return redirect("/goal/list")

    @bp.route("/list", methods=["GET"])
    def goal_list():
        if "token" not in session:
            return render_template("index.html")

        # Init services
        todoist = ServiceTodoist()
        notion = ServiceNotion()
        formatter = ServiceFormatter()

        source = session["source"]
        token = session["token"]
        filter_date = session["filter_date"]

        if source == "Todoist":
            task_list = todoist.get_task_list(token, filter_date)
            project_list = todoist.get_project_list(token)
            task_list = todoist.merge_tasks_projects(task_list, project_list)
            task_list = formatter.calculate_score(task_list)

        elif source == "Notion":
            task_list = notion.get_task_list(token, filter_date)
            task_list = formatter.calculate_score(task_list)

        return render_template("goal_list.html", task_list=task_list)

    @bp.route("/list/download", methods=["GET"])
    def download_goal_list():
        # Init services
        todoist = ServiceTodoist()
        notion = ServiceNotion()
        formatter = ServiceFormatter()

        # Init utils
        dates = UtilsDate()
        files = UtilFile()

        source = session["source"]
        token = session["token"]
        filter_date = session["filter_date"]
        file_name = env["TASK_FILE_NAME"].format(
            timespan=dates.timestamp(env["FILE_TIMESPAN_FORMAT"])
        )

        if source == "Todoist":
            task_list = todoist.get_task_list(token, filter_date)
            project_list = todoist.get_project_list(token)
            task_list = todoist.merge_tasks_projects(task_list, project_list)
            task_list = formatter.calculate_score(task_list)
        elif source == "Notion":
            task_list = notion.get_task_list(token, filter_date)
            task_list = formatter.calculate_score(task_list)

        csv_data = files.json_to_csv(task_list)

        return Response(
            csv_data,
            mimetype="text/csv",
            headers={"Content-Disposition": f"attachment;filename={file_name}"},
        )

from os import environ as env

from flask import Blueprint, render_template, session, redirect, request, Response

from services.formatter import ServiceFormatter
from services.todoist import ServiceTodoist
from services.zenkit import ServiceZenkit
from services.notion import ServiceNotion
from utils.files import UtilFile
from utils.dates import UtilsDate
from environment import DATE_FORMAT_RESULT


class GoalController:
    bp = Blueprint("goal", __name__, url_prefix="/goal")

    @bp.route("/", methods=["GET"])
    def home():
        return redirect("/goal/filter")

    @bp.route("/filter", methods=["GET"])
    def render_goal_filter():
        if "token" not in session:
            return render_template("index.html")

        # Get the list of projects
        project_list = []

        match session["source"]:
            case "Zenkit":
                # Init services
                zenkit = ServiceZenkit(session["token"])
                project_list = zenkit.get_list_of_lists()
                filter_projects = True
            case _:
                filter_projects = False

        return render_template(
            "goal_filter.html",
            project_list=project_list,
            filter_projects=filter_projects,
        )

    @bp.route("/filter", methods=["POST"])
    def goal_filter():
        return redirect(
            "/goal/list?projectList={}&filterDate={}".format(
                request.form.get("selectedProjects"), request.form.get("filterDate")
            )
        )

    @bp.route("/list", methods=["GET"])
    def goal_list():
        if "token" not in session:
            return render_template("index.html")

        # Init services
        formatter = ServiceFormatter()

        source = session["source"]
        token = session["token"]
        filter_date = request.args.get("filterDate")
        project_list = request.args.get("projectList").split(",")
        output = request.args.get("output")
        task_list = []

        match source:
            case "Todoist":
                todoist = ServiceTodoist()
                task_list = todoist.get_task_list(token, filter_date)
                if len(task_list) == 0:
                    return render_template("goal_list.html", task_list=[])
                project_list = todoist.get_project_list(token)
                task_list = todoist.merge_tasks_projects(task_list, project_list)

            case "Notion":
                notion = ServiceNotion()
                task_list = notion.get_task_list(token, filter_date)

            case "Zenkit":
                zenkit = ServiceZenkit(token)
                task_list = []
                for project_id in project_list:
                    column_list = zenkit.get_column_names(project_id)
                    task_list += zenkit.get_entry_list_per_list(
                        project_id, filter_date, column_list
                    )

        # Formatting task list
        task_list = formatter.format_dates(task_list, DATE_FORMAT_RESULT)
        task_list = formatter.calculate_score(task_list)

        if output == "json":
            return task_list
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

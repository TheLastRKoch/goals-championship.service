from os import environ as env
import pandas as pd
import json

from utils.webrequest import UtilWebRequest
from utils.jmespath import UtilsJMESpath


class ServiceTodoist:

    def check_token_auth(self, token):
        # Define Services
        web_request = UtilWebRequest()

        headers = {
            "Authorization": f"Bearer {token}"
        }

        # Check token authtentication
        r = web_request.get(
            headers, None, env["TODOIST_API_URL"]+r"/get_all?limit=1", None)
        if r:
            return True
        return False

    def get_project_list(self, token):
        # Define Services
        web_request = UtilWebRequest()

        headers = {
            "Authorization": f"Bearer {token}"
        }

        url = env["TODOIST_PROJECTS_URL"]
        r = web_request.get(headers, None, url, None)
        return json.loads(r.text)

    def get_task_list(self, token, time_period):
        # Define Services
        web_request = UtilWebRequest()

        headers = {
            "Authorization": f"Bearer {token}"
        }

        # Obtain tasks
        limit = int(env["API_LIMIT"])
        offset = 0
        since = time_period+"T00:00:00"
        task_list = []
        while (True):
            url = env["TODOIST_GET_TASK_URL"].format(
                limit=limit,
                offset=offset,
                since=since
            )
            r = web_request.get(headers, None, url, None)
            body = json.loads(r.text)
            task_list += body["items"]
            offset += limit
            if len(body["items"]) == 0:
                break
        return task_list

    def merge_tasks_projects(self, task_list, project_list):
        # Init utils
        jmespath = UtilsJMESpath()

        task_df = pd.DataFrame(task_list)
        project_df = pd.DataFrame(project_list)

        result_df = pd.merge(task_df, project_df,
                             left_on="project_id", right_on="id")

        result_df = json.loads(result_df.to_json(orient='records'))

        return jmespath.expression(env["TODOIST_TASK_QUERY"], result_df)

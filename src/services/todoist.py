from utils.webrequest import UtilWebRequest
from os import environ as env
import json


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

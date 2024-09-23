from utils.webrequest import UtilWebRequest
from os import environ as env
import json


class ServiceNotion:

    def check_token_auth(self, token):
        # Define Services
        web_request = UtilWebRequest()

        headers = {
            "Authorization": f"Bearer {token}"
        }

        # Check token authtentication
        r = web_request.get(
            headers, None, env["TODOIST_API_URL"]+r"/get_all?page_size=1", None)
        if r:
            return True
        return False

    def get_task_list(self, token, time_period):
        # Define Services
        web_request = UtilWebRequest()

        headers = {
            "Authorization": f"Bearer {token}"
        }

        # Obtain tasks
        database_id = json.loads(env["NOTION_DATABASE_ID"])["Workitems"]
        page_size = int(env["API_LIMIT"])
        cursor = None
        since = time_period+"T00:00:00"
        task_list = []
        continue_paginating = True
        while (continue_paginating):
            url = env["NOTION_GET_TASK_URL"].format(
                database_id=database_id
            )

            payload = json.loads(env[NOTION_PAYLOAD]).format(
                cursor=cursor,
                page_size=page_size,
                since=since
            )

            response = web_request.get(
                headers=headers,
                url=url,
                body=json.dumps(payload)
            )

            # TODO: Make the jmespath filter

            task_list += ["items"]
            cursor = response.json()["next_cursor"]
            if cursor is None:
                continue_paginating = False
        return task_list

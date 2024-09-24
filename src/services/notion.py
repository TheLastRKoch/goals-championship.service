from utils.webrequest import UtilWebRequest
from utils.dates import UtilsDate
from utils.jinja import UtilsJinja
from os import environ as env
import json


class ServiceNotion:

    def check_token_auth(self, token):
        # Define Utils
        web_request = UtilWebRequest()
        dates = UtilsDate()
        jinja = UtilsJinja()

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Notion-Version": env["NOTION_VERSION"]
            }

        database_id = json.loads(env["NOTION_DATABASES"])["Workitems"]
        since = dates.first_day_month(env["NOTION_DATE_FORMAT"])

        url = env["NOTION_GET_TASK_URL"].format(
            database_id=database_id
        )

        payload = json.dumps(json.loads(jinja.render(
            env["NOTION_PAYLOAD"],
            page_size=1,
            since=since
        )))

        response = web_request.post(
            headers=headers,
            url=url,
            payload=payload
        )

        if response.status_code == 200:
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

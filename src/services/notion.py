from os import environ as env
import json

from utils.webrequest import UtilWebRequest
from utils.jmespath import UtilsJMESpath
from utils.dates import UtilsDate
from utils.jinja import UtilsJinja


class ServiceNotion:

    def __get_headers(self, token):
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Notion-Version": env["NOTION_VERSION"]
        }

    def check_token_auth(self, token):
        # Define Utils
        web_request = UtilWebRequest()
        dates = UtilsDate()
        jinja = UtilsJinja()

        database_id = json.loads(env["NOTION_DATABASES"])["Workitems"]
        since = dates.first_day_month(env["NOTION_DATE_FORMAT"])

        headers = self.__get_headers(token)

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
        # Define Utils
        web_request = UtilWebRequest()
        jinja = UtilsJinja()
        jmespath = UtilsJMESpath()

        headers = self.__get_headers(token)

        task_list = []
        database_id = json.loads(env["NOTION_DATABASES"])["Workitems"]
        page_size = env["API_LIMIT"]
        cursor = None
        continue_paginating = True

        while continue_paginating:
            url = env["NOTION_GET_TASK_URL"].format(
                database_id=database_id
            )

            payload = json.dumps(json.loads(jinja.render(
                env["NOTION_PAYLOAD"],
                cursor=cursor,
                page_size=page_size,
                since=time_period
            )))

            response = web_request.post(
                headers=headers,
                url=url,
                payload=payload
            )

            if response.status_code != 200:
                return None

            result = jmespath.expression(
                env["NOTION_TASK_QUERY"], response.json())

            task_list += result

            cursor = response.json()["next_cursor"]

            if cursor is None:
                continue_paginating = False

        return task_list

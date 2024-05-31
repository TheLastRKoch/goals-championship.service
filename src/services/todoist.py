from services.service_jmespath import ServiceJMESpath
from utils.webrequest import UtilWebRequest
from os import environ as env
import json


class ServiceTodoist:

    def filter_by_date(self, task_list, month_label):
        # Service definition
        service_jmespath = ServiceJMESpath()

        return service_jmespath.expression(
            env['LABEL_QUERY'].format(label=month_label),
            task_list
        )

    def get_task_list(self, token, time_period):
        # Define Services
        webrequest = UtilWebRequest()

        headers = {
            "Authorization": f"Bearer {token}"
        }

        # # Check token authtentication
        # if service_request.check_auth(
        #         headers, None, env["BASE_API_URL"]+r"/get_all?limit=1", None):
        # else:
        #     raise Exception("Something went wrong while authenticating")

        # Obtain tasks
        limit = int(env["API_LIMIT"])
        offset = 0
        since = time_period+"T00:00:00"
        task_list = []
        while (True):
            url = env["BASE_GET_TASK_URL"].format(
                limit=limit,
                offset=offset,
                since=since
            )
            r = webrequest.get(headers, None, url, None)
            body = json.loads(r.text)
            task_list += body["items"]
            offset += limit
            if len(body["items"]) == 0:
                return task_list

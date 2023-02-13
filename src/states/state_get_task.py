from services.service_request import ServiceRequest
from services.service_date import ServiceDate
from os import environ as env
import json


class StateGetTasks:

    # TODO: Missing Token validation
    def run(self, token):
        # Define Services
        service_request = ServiceRequest()
        service_date = ServiceDate()

        headers = {
            "Authorization": f"Bearer {token}"
        }

        limit = int(env["API_LIMIT"])
        offset = 0
        since = service_date.first_day_month()
        task_list = []
        while (True):
            url = env["BASE_API_URL"].format(
                limit=limit,
                offset=offset,
                since=since
            )
            r = service_request.get(headers, None, url, None)
            body = json.loads(r.text)
            task_list += body["items"]
            offset += limit
            if len(body["items"]) == 0:
                break
        return task_list

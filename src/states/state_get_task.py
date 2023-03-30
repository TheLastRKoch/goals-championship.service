from services.service_prompt import ServicePrompt
from services.service_request import ServiceRequest
from os import environ as env
import json


class StateGetTasks:

    # TODO: Missing Token validation
    def run(self, token, time_period):
        # Define Services
        service_request = ServiceRequest()
        service_prompt = ServicePrompt()

        headers = {
            "Authorization": f"Bearer {token}"
        }

        # Check token authtentication
        if service_request.check_auth(
                headers, None, env["BASE_API_URL"]+r"/get_all?limit=1", None):
            service_prompt.message("Successfully authenticated via API Token")
        else:
            raise Exception("Something went wrong while authenticating")

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
            r = service_request.get(headers, None, url, None)
            body = json.loads(r.text)
            task_list += body["items"]
            offset += limit
            if len(body["items"]) == 0:
                break
        return task_list

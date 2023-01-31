from services.service_date import ServiceDate
from services.service_request import ServiceRequest
from os import environ as env
import json


def run2():
    # Services
    service_request = ServiceRequest()
    service_date = ServiceDate()

    headers = {
        "Authorization": f"Bearer {env['TODOIST_API_SECRET']}"
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
    with open("resources/view.json", "w") as outfile:
        outfile.write(json.dumps(task_list))


def run():
    pass


if __name__ == "__main__":
    run2()

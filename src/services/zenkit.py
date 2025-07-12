from utils.jmespath import UtilsJMESpath
from os import environ as env
import requests


class ServiceZenkit:
    def __init__(self, api_token):

        # Define services
        self.jmespath = UtilsJMESpath()

        self.headers = {
            "Zenkit-API-Key": api_token,
            "Content-Type": "application/json",
        }
        self.base_url = env["ZENKIT_BASE_URL"]

        self.items_per_page = int(env["ZENKIT_ITEMS_PER_PAGE"])

    def check_token_auth(self):
        url = self.base_url + "/users/me"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return True
        return False

    def get_list_element(self, list_id):
        url = self.base_url + f"/lists/{list_id}/elements"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()

        return response.json()

    def get_done_stage(self, list_id):
        url = self.base_url + f"/lists/{list_id}/elements"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()

        return self.jmespath.expression(
            env["ZENKIT_GET_DONE_CATEGORY"],
            response.json(),
        )

    def get_list_of_lists(self):
        url = self.base_url + "/users/me/workspacesWithLists"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()

        # Format the request
        return self.jmespath.expression(env["ZENKIT_LIST_QUERY"], response.json())

    def get_list_columns(self, list_id):
        url = self.base_url + f"/lists/{list_id}/elements"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()

        columns_dic = {}

        for item in response.json():
            resource_role = item.get("resourceRole")
            element_id = item.get("id")
            uuid = item.get("uuid")

            columns_dic.update(
                {
                    f"{resource_role}_{record}": {
                        "id": element_id,
                        "column_name": f"{uuid}_{record}",
                    }
                    for record in item.get("businessData", [])
                }
            )
        return columns_dic

    def get_entry_list_per_list(
        self, list_id, column_list, done_category_id, start_date, end_date
    ):
        skip = 0
        keep = True
        due_date_id = column_list.get("dueDate_date").get("id")
        stage_id = column_list.get("stage_categories_sort").get("id")
        url = f"{self.base_url}/lists/{list_id}/entries/filter"
        entry_list = []

        while keep:

            # TODO
            # - Get the filter categories for each list
            payload = {
                "filter": {
                    "AND": {
                        "TERMS": [
                            {
                                "elementId": stage_id,
                                "modus": "equals",
                                "negated": False,
                                "filterCategories": [done_category_id],
                            },
                            {
                                "elementId": due_date_id,
                                "modus": "contains",
                                "negated": False,
                                "dateType": 10,
                                "dateFrom": f"{start_date}T12:00:00.000Z",
                                "dateTo": f"{end_date}T12:00:00.000Z",
                            },
                        ]
                    }
                },
                "limit": self.items_per_page,
                "skip": skip,
            }

            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            if response.json() == []:
                keep = False
            skip += self.items_per_page
            entry_list += response.json()

        # Format response
        return self.jmespath.expression(
            env["ZENKIT_ENTRIES_QUERY"]
            .replace("@{due_date}", column_list.get("dueDate_date").get("column_name"))
            .replace("@{project}", column_list.get("tags_categories_sort").get("column_name")),
            entry_list,
        )

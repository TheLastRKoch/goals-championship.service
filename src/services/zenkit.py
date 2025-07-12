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
            column_list += [
                columns_dic[f"{resource_role}_{record}"] = {
                        "id": element_id,
                        "column_name": f"{uuid}_{record}",
                    }
                for record in item.get("businessData")
            ]

        return column_list

    def get_entry_list_per_list(
        self, list_id, column_list, element_list, start_date, end_date
    ):
        skip = 0
        keep = True
        due_date_id = [
            element.get("id")
            for element in element_list
            if element.get("resourceRole") == "dueDate"
        ][0]
        stage_id = [
            element.get("id")
            for element in element_list
            if element.get("resourceRole") == "stage"
        ][0]
        url = f"{self.base_url}/lists/{list_id}/entries/filter/list"
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
                                "filterCategories": [15058603],
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
            if response.json().get("listEntries") == []:
                keep = False
            skip += self.items_per_page
            entry_list += response.json().get("listEntries")

        # Format response
        return self.jmespath.expression(
            env["ZENKIT_ENTRIES_QUERY"]
            .replace("@{due_date}", column_list.get("start_date"))
            .replace("@{project}", column_list.get("project")),
            entry_list,
        )

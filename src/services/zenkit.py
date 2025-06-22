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

    def get_list_of_lists(self):
        url = self.base_url + "/users/me/workspacesWithLists"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()

        # Format the request
        return self.jmespath.expression(env["ZENKIT_LIST_QUERY"], response.json())

    def get_entry_list_per_list(self, list_short_id, start_date):
        skip = 0
        keep = True
        url = f"{self.base_url}/lists/{list_short_id}/entries/filter"
        entry_list = []

        while keep:
            payload = {"limit": self.items_per_page, "skip": skip}
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            if response.json() == []:
                keep = False
            skip += self.items_per_page
            entry_list += response.json()

        # Format response
        return self.jmespath.expression(
            env["ZENKIT_ENTRIES_QUERY"].replace("@{selected_date}", start_date),
            entry_list,
        )

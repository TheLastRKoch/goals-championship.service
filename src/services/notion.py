'''Notion service module.

This module provides services for interacting with the Notion API to
retrieve task lists.
'''

import json
from os import environ as env

from utils.webrequest import UtilWebRequest
from utils.jmespath import UtilsJMESpath
from utils.dates import UtilsDate
from utils.jinja import UtilsJinja


class ServiceNotion:
    '''Service for interacting with Notion.'''

    def __get_headers(self, token):
        '''Constructs headers for Notion API requests.

        Args:
            token (str): The Notion API token.

        Returns:
            dict: The request headers.
        '''
        return {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
            'Notion-Version': env['NOTION_VERSION']
        }

    def check_token_auth(self, token):
        '''Checks if the provided Notion token is valid.

        Args:
            token (str): The Notion API token.

        Returns:
            bool: True if authentication is successful, False otherwise.
        '''
        # Define Utils
        web_request = UtilWebRequest()
        dates = UtilsDate()
        jinja = UtilsJinja()

        database_id = json.loads(env['NOTION_DATABASES'])['Workitems']
        since = dates.first_day_month(env['NOTION_DATE_FORMAT'])

        headers = self.__get_headers(token)

        url = env['NOTION_GET_TASK_URL'].format(
            database_id=database_id
        )

        payload = json.dumps(json.loads(jinja.render(
            env['NOTION_PAYLOAD'],
            page_size=1,
            since=since
        )))

        response = web_request.post(
            headers=headers,
            url=url,
            payload=payload
        )

        return response.status_code == 200

    def get_task_list(self, token, time_period):
        '''Retrieves a list of tasks from Notion for a specific time period.

        Args:
            token (str): The Notion API token.
            time_period (str): The time period filter.

        Returns:
            list: A list of tasks retrieved from Notion.
        '''
        # Define Utils
        web_request = UtilWebRequest()
        jinja = UtilsJinja()
        utils_jmespath = UtilsJMESpath()

        headers = self.__get_headers(token)

        task_list = []
        database_id = json.loads(env['NOTION_DATABASES'])['Workitems']
        page_size = env['API_LIMIT']
        cursor = None
        continue_paginating = True

        while continue_paginating:
            url = env['NOTION_GET_TASK_URL'].format(
                database_id=database_id
            )

            payload = json.dumps(json.loads(jinja.render(
                env['NOTION_PAYLOAD'],
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

            result = utils_jmespath.expression(
                env['NOTION_TASK_QUERY'], response.json())

            task_list += result

            cursor = response.json().get('next_cursor')

            if cursor is None:
                continue_paginating = False

        return task_list

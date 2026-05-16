'''Todoist service module.

This module provides services for interacting with the Todoist API to
retrieve tasks and projects.
'''

import json
from os import environ as env

import pandas as pd

from utils.webrequest import UtilWebRequest
from utils.jmespath import UtilsJMESpath


class ServiceTodoist:
    '''Service for interacting with Todoist.'''

    def check_token_auth(self, token):
        '''Checks if the provided Todoist token is valid.

        Args:
            token (str): The Todoist API token.

        Returns:
            bool: True if authentication is successful, False otherwise.
        '''
        # Define Services
        web_request = UtilWebRequest()

        headers = {
            'Authorization': f'Bearer {token}'
        }

        # Check token authentication
        response = web_request.get(
            headers, None, f"{env['TODOIST_API_URL']}/get_all?limit=1", None)
        return bool(response)

    def get_project_list(self, token):
        '''Retrieves a list of projects from Todoist.

        Args:
            token (str): The Todoist API token.

        Returns:
            list: A list of projects.
        '''
        # Define Services
        web_request = UtilWebRequest()

        headers = {
            'Authorization': f'Bearer {token}'
        }

        url = env['TODOIST_PROJECTS_URL']
        response = web_request.get(headers, None, url, None)
        return json.loads(response.text)

    def get_task_list(self, token, start_date):
        '''Retrieves a list of completed tasks from Todoist since a given date.

        Args:
            token (str): The Todoist API token.
            start_date (str): The start date in YYYY-MM-DD format.

        Returns:
            list: A list of tasks.
        '''
        # Define Services
        web_request = UtilWebRequest()

        headers = {
            'Authorization': f'Bearer {token}'
        }

        # Obtain tasks
        limit = int(env['API_LIMIT'])
        offset = 0
        since = f'{start_date}T00:00:00'
        task_list = []
        while True:
            url = env['TODOIST_GET_TASK_URL'].format(
                limit=limit,
                offset=offset,
                since=since
            )
            response = web_request.get(headers, None, url, None)
            body = json.loads(response.text)
            task_list += body['items']
            offset += limit
            if not body['items']:
                return task_list

    def merge_tasks_projects(self, task_list, project_list):
        '''Merges tasks with their corresponding projects and filters the result.

        Args:
            task_list (list): The list of tasks.
            project_list (list): The list of projects.

        Returns:
            list: The merged and filtered task list.
        '''
        # Init utils
        utils_jmespath = UtilsJMESpath()

        task_df = pd.DataFrame(task_list)
        project_df = pd.DataFrame(project_list)

        result_df = pd.merge(task_df, project_df,
                             left_on='project_id', right_on='id')

        result_list = json.loads(result_df.to_json(orient='records'))

        return utils_jmespath.expression(env['TODOIST_TASK_QUERY'], result_list)

'''Formatter service module.

This module provides services for formatting task data, including dates
and score calculations.
'''

import json
from datetime import datetime
from os import environ as env

import pandas as pd
import jmespath


class ServiceFormatter:
    '''Service for formatting task lists and calculating scores.'''

    def __filter(self, query, task_list):
        '''Filters a list using a JMESPath query.

        Args:
            query (str): The JMESPath query string.
            task_list (list): The list to search.

        Returns:
            list: The filtered results.
        '''
        engine = jmespath.compile(query)
        return engine.search(task_list)

    def assign_value(self, content):
        '''Assigns a score value to a task based on its description content.

        Args:
            content (str): The description of the task.

        Returns:
            int: The score value assigned to the task.
        '''
        task_values = json.loads(env['LIST_TASK_CATEGORY'])
        for value in task_values:
            if value['tag'] in content:
                return value['value']
        return 1

    def calculate_score(self, task_list):
        '''Calculates scores for all tasks in the list.

        Args:
            task_list (list): The list of tasks.

        Returns:
            list: The task list with scores added.
        '''
        if not task_list:
            return []
        task_df = pd.DataFrame(task_list)
        task_df['Score'] = task_df['Description'].apply(self.assign_value)
        return json.loads(task_df.to_json(orient='records'))

    def format_dates(self, task_list, date_format):
        '''Formats completion dates for all tasks in the list.

        Args:
            task_list (list): The list of tasks.
            date_format (str): The target date format string.

        Returns:
            list: The task list with formatted dates.
        '''
        for task in task_list:
            task_completed_at = task.get('Completed at')
            if task_completed_at:
                completed_at_dt = datetime.fromisoformat(
                    task_completed_at.replace('Z', '+00:00')
                )
                formatted_date = completed_at_dt.strftime(date_format)
                task['Completed at'] = formatted_date
        return task_list

    def get_start_date(self, month, year):
        '''Constructs a start date string for a given month and year.

        Args:
            month (str): The month.
            year (str): The year.

        Returns:
            str: The start date in YYYY-MM-DD format.
        '''
        return f'{year}-{month}-01'

    def get_end_date(self, month, year):
        '''Constructs an end date string for a given month and year.

        Args:
            month (str): The month.
            year (str): The year.

        Returns:
            str: The end date in YYYY-MM-DD format.
        '''
        return f'{year}-{month}-31'

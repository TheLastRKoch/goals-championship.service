'''Score calculation service module.

This module provides the service to calculate scores for tasks based on
categories defined in environment variables.
'''

import json
from os import environ as env

from utils.jmespath import UtilsJMESpath


class ServiceCalculateScore:
    '''Service for calculating task scores.'''

    def run(self, task_list, month_label):
        '''Calculates category scores and total score for a list of tasks.

        Args:
            task_list (list): The list of tasks to score.
            month_label (str): The month label for the query.

        Returns:
            tuple: A list of scores per category and the total score.
        '''
        # Service Definition
        utils_jmespath = UtilsJMESpath()

        # Calculate category score
        score_list = json.loads(env['LIST_TASK_CATEGORY'])
        total_score = 0

        for category in score_list:
            query = env['CATEGORY_TASK_QUERY'].format(
                month_label=month_label,
                category=category['tag']
            )
            category_task = utils_jmespath.expression(query, task_list)
            score = len(category_task) * category['value']
            category['score'] = score
            total_score += score

        # Calculate simple score
        query = env['SIMPLE_TASK_QUERY']
        simple_task = utils_jmespath.expression(query, task_list)
        score = len(simple_task) * 1
        score_list.append(
            {
                'tag': 'Simple',
                'score': score
            }
        )
        total_score += score
        return score_list, total_score

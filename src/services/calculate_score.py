from services.service_jmespath import ServiceJMESpath
from os import environ as env
import json


class ServiceCalculateScore:

    def run(self, task_list, month_label):

        # Service Definition
        service_jmespath = ServiceJMESpath()

        # Calculate category score
        score_list = json.loads(env["LIST_TASK_CATEGORY"])
        total_score = 0

        for category in score_list:
            query = env["CATEGORY_TASK_QUERY"].format(
                month_label=month_label,
                category=category["tag"]
            )
            category_task = service_jmespath.expression(query, task_list)
            score = len(category_task) * category["value"]
            category["score"] = score
            total_score += score

        # Calculate simple score
        query = env["SIMPLE_TASK_QUERY"]
        simple_task = service_jmespath.expression(query, task_list)
        score = len(simple_task) * 1
        score_list.append(
            {
                "tag": "Simple",
                "score": score
            }
        )
        total_score += score
        return score_list, total_score

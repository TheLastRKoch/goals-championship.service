from os import environ as env
import pandas as pd
import jmespath
import json
import numpy as np


class ServiceFormatter:
    def __filter(self, query, list):
        engine = jmespath.compile(query)
        return engine.search(list)

    def assign_value(self, content):
        task_values = json.loads(env["LIST_TASK_CATEGORY"])
        for value in task_values:
            if value["tag"] in content:
                return value["value"]
        return 1

    def calculate_score(self, task_list):
        task_df = pd.DataFrame(task_list)
        task_df['Score'] = task_df['Description'].apply(
            lambda x: self.assign_value(x))
        return json.loads(task_df.to_json(orient='records'))

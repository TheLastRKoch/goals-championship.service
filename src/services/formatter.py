from datetime import datetime
from os import environ as env
import json

import pandas as pd
import jmespath


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
        task_df["Score"] = task_df["Description"].apply(lambda x: self.assign_value(x))
        return json.loads(task_df.to_json(orient="records"))

    def format_dates(self, task_list, date_format):
        for task in task_list:
            task_completed_at = task.get("Completed at")
            completed_at_dt = datetime.fromisoformat(
                task_completed_at.replace("Z", "+00:00")
            )
            formatted_date = completed_at_dt.strftime(date_format)
            task["Completed at"] = formatted_date
        return task_list

    def get_start_date(self, month, year):
        return f"{year}-{month}-01"

    def get_end_date(self, month, year):
        return f"{year}-{month}-31"

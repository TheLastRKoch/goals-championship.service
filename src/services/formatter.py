from os import environ as env
import pandas as pd
import jmespath
import json


class ServiceFormatter:
    def __filter(self, query, list):
        engine = jmespath.compile(query)
        return engine.search(list)

    def merge_tasks_projects(self, task_list, project_list):
        task_df = pd.DataFrame(task_list)
        project_df = pd.DataFrame(project_list)

        result = pd.merge(task_df, project_df,
                          left_on="project_id", right_on="id")
        result = json.loads(result.to_json(orient='records'))

        # Format the payload
        return self.__filter(env["FORMAT_TASK_QUERY"], result)

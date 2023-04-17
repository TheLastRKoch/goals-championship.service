from services.service_jmespath import ServiceJMESpath
from os import environ as env


class StateFilterTasks:

    def run(self, task_list, month_label):
        # Service definition
        service_jmespath = ServiceJMESpath()

        return service_jmespath.expression(
            env['LABEL_QUERY'].format(label=month_label),
            task_list
        )

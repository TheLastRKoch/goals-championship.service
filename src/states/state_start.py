from services.service_file import ServiceFile
from states.state_get_task import StateGetTasks

from states.state_calculate_score import StateCalculateScore
import json


class StateStart:

    def run(self):
        # Define Services
        service_file = ServiceFile()

        # Define States
        get_tasks = StateGetTasks()
        calculate_score = StateCalculateScore()

        task_list = get_tasks.run()
        service_file.write_text_file(
            "resources/view.json", json.dumps(task_list))
        calculate_score.run(task_list, "Febrero")

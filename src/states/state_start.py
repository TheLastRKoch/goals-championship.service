from states.state_calculate_score import StateCalculateScore
from services.service_prompt import ServicePrompt
from states.state_filter_tasks import StateFilterTasks
from states.state_get_task import StateGetTasks
import json


class StateStart:

    def run(self):
        keep = True
        i = 0
        while (keep):
            try:
                # Define Services
                service_prompt = ServicePrompt()

                # Define States
                get_tasks = StateGetTasks()
                calculate_score = StateCalculateScore()
                filter_tasks = StateFilterTasks()

                service_prompt.welcome()
                token = service_prompt.ask_user_token()
                month_label = service_prompt.ask_month_label()
                time_period = service_prompt.ask_time_period()

                # Get all task from API
                task_list = get_tasks.run(token, time_period)

                # Filter by Label
                filtered_task_list = filter_tasks.run(task_list, month_label)

                score_list, total_score = calculate_score.run(
                    filtered_task_list, month_label)

                service_prompt.message("\n\nFinal Score:\n"+str(total_score))
                service_prompt.print_score_list(score_list)
                if service_prompt.ask_show_complete_json() == "y":
                    service_prompt.message(
                        "\n\nAll tasks:\n"+json.dumps(task_list, indent=2))

                keep = False
            except Exception as err:
                service_prompt.message_wait("Error: "+str(err))
                if i < 3:
                    i += 1
                else:
                    keep = False

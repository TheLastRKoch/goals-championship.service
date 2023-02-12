from states.state_calculate_score import StateCalculateScore
from services.service_jmespath import ServiceJMESpath
from services.service_file import ServiceFile
from dotenv import load_dotenv
from os import environ as env
import json


def run():
    import json
    your_list_of_dict = [{"test": "test", "score": 1},
                         {"test": "test1", "score": 2}]
    with open("resources/view.txt", 'w') as f:
        json.dump(your_list_of_dict, f)


def run2():
    view = json.loads(env["LIST_TASK_CATEGORY"])
    stop = ""


def run3():
    service_jmespath = ServiceJMESpath()
    service_file = ServiceFile()

    custom_json = json.loads(service_file.read_text_file("resources/view.json"))
    view = service_jmespath.expression("[].id", custom_json)
    stop = ""

    


if __name__ == "__main__":
    # Load env variables
    load_dotenv()

    # State Services
    calculate_score = StateCalculateScore()
    # calculate_score.run("Febrero")
    run3()

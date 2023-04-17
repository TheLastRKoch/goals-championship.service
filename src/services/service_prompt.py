from services.service_command import ServiceCommand
from services.service_file import ServiceFile
from os import environ as env
import pwinput


class ServicePrompt:

    def welcome(self):
        # Define services
        service_command = ServiceCommand()
        service_file = ServiceFile()

        greating_message = service_file.read_text_file(env["GREATING_PATH"])
        service_command.clear_screen()
        print(greating_message)

    def ask_user_token(self):
        return pwinput.pwinput(prompt="\n\nPlease type the user token\n", mask="*")

    def ask_month_label(self):
        return input("\n\nPlease type the month label to query\n")

    def ask_time_period(self):
        return input("\n\nPlease type the period to query (YYYY-M-D)\n")

    def ask_show_complete_json(self):
        return input("\n\nDo you want to see the complete JSON response (y/n)\n")

    def message_wait(self, message):
        print("\n"+message+"\n\n")
        input("Press Any key to continue ...")

    def message(self, text):
        print("\n"+text+"\n\n")

    def print_score_list(self, score_list: list[dict]):
        for score in score_list:
            print(f"{score['tag']}: {score['score']}")

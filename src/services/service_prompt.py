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

    def message_wait(self, message):
        print("\n"+message+"\n\n")
        input("Press Any key to continue ...")

    def message(self, text):
        print("\n"+text+"\n\n")

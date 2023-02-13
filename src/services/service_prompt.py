from services.service_command import ServiceCommand
from services.service_file import ServiceFile
from os import environ as env
import getpass


class ServicePrompt:

    def welcome(self):
        # Define services
        service_command = ServiceCommand()
        service_file = ServiceFile()

        greating_message = service_file.read_text_file(env["GREATING_PATH"])
        service_command.clear_screen()
        print(greating_message)

    def ask_user_token(self):
        return getpass.getpass("\n\nPlease type the user token\n")

    def ask_month_label(self):
        return input("\n\nPlease type the month label to query\n")

    def ask_period(self):
        return input("\n\nPlease type the period to query (DD/MM/YYYY)\n")

    def message(self, text):
        print(text)

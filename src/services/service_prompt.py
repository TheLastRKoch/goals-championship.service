from services.service_command import ServiceCommand


class ServicePrompt:

    def welcome(self):
        service_prompt = ServiceCommand()
        service_prompt.clear_screen()
        print()
    
    def ask_user_token(self):
        return input("Please type the user token")

    

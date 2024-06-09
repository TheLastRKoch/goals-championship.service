from controllers.goals import GoalController, GoalListController
from controllers.login import LoginController
from dotenv import load_dotenv
from os import environ as env
from flask import Flask
import os

# Load env variables
load_dotenv()


app = Flask(__name__, template_folder=env["TEMPLATES_PATH"])
app.secret_key = os.getenv("SECRET_KEY")

# Register controllers
app.add_url_rule('/login', view_func=LoginController.as_view('login'))


if __name__ == "__main__":
    app.run(
        host=os.getenv("HOSTNAME"),
        port=int(os.getenv("PORT")),
        debug=bool(os.getenv("DEBUG"
                             )))

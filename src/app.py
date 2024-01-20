from controllers.goals import GoalController, GoalListController
from controllers.index import IndexController
from controllers.login import LoginController
from dotenv import load_dotenv
from flask import Flask
import os

# Load env variables
load_dotenv()

app = Flask(__name__, template_folder="ui/templates")

app.secret_key = os.getenv("SECRET_KEY")

app.add_url_rule(
    "/", view_func=IndexController.as_view("home"),
    methods=['GET'])

app.add_url_rule(
    "/login", view_func=LoginController.as_view("login"),
    methods=['GET', 'POST'])

app.add_url_rule(
    "/goals", view_func=GoalController.as_view("goals"),
    methods=['GET', 'POST'])

app.add_url_rule(
    "/goal/list", view_func=GoalListController.as_view("goalList"),
    methods=['GET', 'POST'])

if __name__ == "__main__":
    app.run(
        host=os.getenv("HOSTNAME"),
        port=int(os.getenv("PORT")),
        debug=bool(os.getenv("DEBUG"
                             )))

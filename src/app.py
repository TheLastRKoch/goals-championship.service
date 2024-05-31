from controllers.goals import GoalController, GoalListController
from controllers.index import IndexController
from controllers.login import LoginController
from dotenv import load_dotenv
from flask import Flask
import os

# Load env variables
load_dotenv()

app = Flask(__name__, template_folder="ui/templates")

endpoint_list = [
    {
        "path": "/",
        "source": IndexController.as_view("home"),
        "methods": ['GET']
    },
    {
        "path": "/login",
        "source": LoginController.as_view("login"),
        "methods": ['GET', 'POST']
    },
    {
        "path": "/goals",
        "source": GoalController.as_view("goals"),
        "methods": ['GET', 'POST']
    },
    {
        "path": "/goal/list",
        "source": GoalListController.as_view("goalList"),
        "methods": ['GET', 'POST']
    }
]

for endpoint in endpoint_list:

    app.add_url_rule(
        endpoint["path"],
        view_func=endpoint["source"],
        methods=endpoint["methods"]
    )

app.secret_key = os.getenv("SECRET_KEY")

if __name__ == "__main__":
    app.run(
        host=os.getenv("HOSTNAME"),
        port=int(os.getenv("PORT")),
        debug=bool(os.getenv("DEBUG"
                             )))

from controllers.goals import GoalController, GoalListController, DownloadGoalList
from controllers.account import LoginController, LogoutController
from controllers.index import IndexController
from dotenv import load_dotenv
from os import environ as env
from flask import Flask
import os


# Load env variables
load_dotenv()


app = Flask(__name__, template_folder=env["TEMPLATES_PATH"])
app.secret_key = os.getenv("SECRET_KEY")

# Register controllers
app.add_url_rule('/', view_func=IndexController.as_view('index'))
app.add_url_rule('/account/login', view_func=LoginController.as_view('login'))
app.add_url_rule('/account/logout', view_func=LogoutController.as_view('logout'))
app.add_url_rule('/goals', view_func=GoalController.as_view('goals'))
app.add_url_rule('/goal/list', view_func=GoalListController.as_view('goal_list'))
app.add_url_rule('/goal/list/download', view_func=DownloadGoalList.as_view('goal_list_download'))


if __name__ == "__main__":
    app.run(
        host=os.getenv("HOSTNAME"),
        port=int(os.getenv("PORT")),
        debug=bool(os.getenv("DEBUG"
                             )))

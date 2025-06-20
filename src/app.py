from os import environ as env
import os

from dotenv import load_dotenv
from flask import Flask

from controllers.account import AccountController
from controllers.index import IndexController
from controllers.goal import GoalController


# Load env variables
load_dotenv()

app = Flask(__name__, template_folder=env["TEMPLATES_PATH"])
app.secret_key = os.getenv("SECRET_KEY")

# Init controllers
account_controller = AccountController()
index_controller = IndexController()
goal_controller = GoalController()

# Register blueprints
app.register_blueprint(goal_controller.bp)
app.register_blueprint(account_controller.bp)
app.register_blueprint(index_controller.bp)

if __name__ == "__main__":
    app.run(
        host=os.getenv("HOSTNAME"),
        port=int(os.getenv("PORT")),
        debug=bool(os.getenv("DEBUG")),
    )

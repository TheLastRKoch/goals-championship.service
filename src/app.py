'''Main application entry point.

This module initializes the Flask application, configures settings,
and registers the controller blueprints.
'''

from flask import Flask

from environment import TEMPLATES_PATH, SECRET_KEY, HOSTNAME, PORT, DEBUG_MODE
from controllers.account import AccountController
from controllers.index import IndexController
from controllers.goal import GoalController


app = Flask(__name__, template_folder=TEMPLATES_PATH)
app.secret_key = SECRET_KEY

# Init controllers
account_controller = AccountController()
index_controller = IndexController()
goal_controller = GoalController()

# Register blueprints
app.register_blueprint(goal_controller.bp)
app.register_blueprint(account_controller.bp)
app.register_blueprint(index_controller.bp)

if __name__ == '__main__':
    app.run(
        host=HOSTNAME,
        port=PORT,
        debug=DEBUG_MODE,
    )

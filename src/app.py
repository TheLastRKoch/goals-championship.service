from controllers.index import IndexController
from states.state_start import StateStart
from dotenv import load_dotenv
from flask import Flask
import os

# Load env variables
load_dotenv()

# State Definition
# start = StateStart()
# start.run()


app = Flask(__name__, template_folder="ui/templates")

app.add_url_rule(
    "/", view_func=IndexController.as_view("home"), methods=['GET'])

if __name__ == "__main__":
    app.run(
        host=os.getenv("HOSTNAME"),
        port=int(os.getenv("PORT")),
        debug=bool(os.getenv("DEBUG"
                             )))

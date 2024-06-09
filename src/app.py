from controllers.goals import GoalController, GoalListController
from controllers.index import IndexController
from dotenv import load_dotenv
from flask import Flask
import os

from flask import render_template, request, session, redirect, url_for
from flask.views import MethodView
from os import environ as env

# Load env variables
load_dotenv()


app = Flask(__name__, template_folder=env["TEMPLATES_PATH"])

@app.route("/login")
def login():
    template_path = env["TEMPLATES_PATH"]+"login.jinja2"
    return render_template("login.jinja2")

@app.route("/login", methods=["POST"])
def procesing_login():
    token = request.form["token"]
    #TODO: Check if token is valid if not show an error
    return {"msg":"Login successfully"}

app.secret_key = os.getenv("SECRET_KEY")

if __name__ == "__main__":
    app.run(
        host=os.getenv("HOSTNAME"),
        port=int(os.getenv("PORT")),
        debug=bool(os.getenv("DEBUG"
                             )))

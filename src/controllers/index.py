from flask import Blueprint, render_template, redirect, session
from flask.views import MethodView


class IndexController:
    bp = Blueprint("index", __name__, url_prefix="/")

    @bp.route("/", methods=["GET"])
    def get():
        if "token" in session.keys():
            return redirect("goal")
        return redirect("account/login")

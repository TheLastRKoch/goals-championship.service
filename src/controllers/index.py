from flask.views import MethodView
from flask import render_template, redirect


class IndexController(MethodView):
    def get(self):
        return redirect("/login")
    # def get(self):
    #     title = "This is a test"
    #     description = "You got it"
    #     return render_template(
    #         "home.html",
    #         title=title,
    #         description=description)

from datetime import datetime
from os import environ as env


class UtilsDate():
    def timestamp(self):
        return datetime.now().strftime(env["DATE_FORMAT"])

    def first_day_month(self):
        month = datetime.now().month
        year = datetime.now().year
        return f"{year}-{month}-1T00:00:00"

    def first_day_custom(self, month, year):
        return f"{year}-{month}-1T00:00:00"

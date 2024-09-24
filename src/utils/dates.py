from datetime import datetime
from os import environ as env


class UtilsDate():
    def timestamp(self, format):
        return datetime.now().strftime(format)

    def first_day_month(self, format):
        month = datetime.now().month
        year = datetime.now().year
        return datetime(year, month, 1).strftime(format)

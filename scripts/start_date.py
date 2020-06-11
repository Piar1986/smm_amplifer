import datetime
from dateutil.relativedelta import relativedelta


def calculate_start_date(days_count, months_count):
    today = datetime.datetime.today()
    start_date = today - relativedelta(days = days_count, months = months_count)
    return start_date
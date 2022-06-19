from dateutil import tz
from pytz import timezone


def get_local_timezone():
    return tz.tzlocal()


def get_eastern_timezone():
    return timezone('US/Eastern')


def get_pacific_timezone():
    return timezone('US/Pacific')

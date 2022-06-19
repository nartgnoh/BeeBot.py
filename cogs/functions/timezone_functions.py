import pytz

from dateutil import tz
from pytz import timezone


# gets BeeBot's local time
def get_local_timezone():
    return tz.tzlocal


def get_eastern_timezone():
    return timezone('US/Eastern')


def get_pacific_timezone():
    return timezone('US/Pacific')


def get_timezone_by_name(timezone_name):
    if timezone_name in pytz.all_timezones:
        return timezone(timezone_name)
    return timezone(get_local_timezone)


def list_all_timezones():
    return pytz.all_timezones
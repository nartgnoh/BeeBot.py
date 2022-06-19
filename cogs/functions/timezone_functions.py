from dateutil import tz
from pytz import timezone


def get_local_timezone():
    return timezone('US/Eastern')

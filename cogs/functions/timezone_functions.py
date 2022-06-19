from dateutil import tz
import pytz


def get_local_timezone():
    return tz.tzlocal()

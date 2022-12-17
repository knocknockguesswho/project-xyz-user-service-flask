import datetime
import platform
import subprocess
import re
import time
from dateutil import tz
# TODO: need to move all to app/utils
_TIME_FORMAT_ = '%Y-%m-%d %H:%M:%S'
_DATE_FORMAT_ = '%Y-%m-%d'
_UTC_TIMEZONE_ = tz.tzutc()
_LOCAL_TIMEZONE_ = tz.tzlocal()
_TIMEZONE_INFO_ = datetime.datetime.now(
    datetime.timezone(datetime.timedelta(0))).astimezone().tzinfo

# def encrypt(data: bytes, key: bytes) -> bytes:
#   algorithm=hashlib.sha256
#   return hmac.new(key,data,algorithm).digest()


def myping(host):
  param = '-n' if platform.system().lower() == 'windows' else '-c'
  command = ['ping', param, '1', host]
  response = subprocess.call(command)
  if response == 0:
    return True
  else:
    return False

def get_age(birth_date: str) -> int:
    """birth_date='1990-01-01 00:00:00'"""
    now = datetime.datetime.now()
    dob = datetime.datetime(*map(int,str(birth_date).split()[0].split('-')))
    return (now-dob).days//365


def is_valid_email(string: str) -> bool:
    return bool(re.search('^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$', string))


def is_valid_date(string: str) -> bool:
    """YYYY-mm-dd from 1900"""
    return bool(re.search('^(19|20)\d\d[- /.](0[1-9]|1[012])[- /.](0[1-9]|[12][0-9]|3[01])$', string))


def default_or_int(default: int, input: str = None):
    if input is None:
        return default
    if len(input) > 0 and input.isdigit() == False:
        return default
    return int(input)

def default_or_str(default: str, input: str = None):
  if input is None:
    return default
  if len(input) == 0:
    return default
  return str(input)

def to_snake_case(string: str) -> str:
    return '-'.join(string.split()).lower()


def snake_to_title_case(string: str) -> str:
    return ' '.join(string.split('_'))


def to_datetime_string(ts: float) -> str:
    return datetime.datetime.fromtimestamp(ts).strftime(_TIME_FORMAT_)


def to_date_string(ts: float) -> str:
    return datetime.datetime.fromtimestamp(ts).strftime(_DATE_FORMAT_)


def to_timestamp(datetime_string: str) -> float:
    """`datetime_string`: YYYY-mm-dd"""
    el = datetime.datetime.strptime(datetime_string, _TIME_FORMAT_)
    return time.mktime(el.timetuple())


def datetime_string_local_time(datetime_string: str) -> str:
    return datetime.datetime.fromisoformat(datetime_string).replace(tzinfo=_UTC_TIMEZONE_).astimezone(_LOCAL_TIMEZONE_)


def datetime_string_utc_time(datetime_string: str) -> str:
    return datetime.datetime.fromisoformat(datetime_string).replace(tzinfo=_LOCAL_TIMEZONE_).astimezone(_UTC_TIMEZONE_)


def timestamp_local_time(ts: float) -> float:
    return datetime.datetime.fromtimestamp(ts).replace(tzinfo=_UTC_TIMEZONE_).astimezone(_LOCAL_TIMEZONE_).timestamp()


def timestamp_utc_time(ts: float, from_timezone: datetime.tzinfo = _LOCAL_TIMEZONE_) -> float:
    return datetime.datetime.fromtimestamp(ts).replace(tzinfo=from_timezone).astimezone(_UTC_TIMEZONE_).timestamp()

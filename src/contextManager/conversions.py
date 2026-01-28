from datetime import datetime
from mariadb.constants import FIELD_TYPE, INDICATOR


"""Create Conversion Functions"""


def convert_to_string(s):
    return str(s)


def convert_to_int(s):
    return int(s)


def convert_to_float(s):
    return float(s)


def convert_to_set(s):
    return {value for value in s}


def convert_to_datetime(s):
    format_string = "%Y-%m-%d %H:%M:%S"
    return datetime.strptime(s, format_string)


def convert_to_date(s):
    format_string = "%Y-%m-%d"
    return datetime.strptime(s, format_string).date()


def none_to_mariadb_none(s):
    return INDICATOR.NULL


conversions = {
    **{FIELD_TYPE.LONG: convert_to_float},
    **{FIELD_TYPE.NULL: none_to_mariadb_none},
    **{FIELD_TYPE.LONGLONG: convert_to_float},
    **{FIELD_TYPE.DATETIME: convert_to_datetime},
    **{FIELD_TYPE.DATETIME2: convert_to_datetime},
    **{FIELD_TYPE.DATE: convert_to_date},
}

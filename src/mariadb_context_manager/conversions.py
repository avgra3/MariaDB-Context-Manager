from datetime import datetime
from mariadb.constants import FIELD_TYPE, INDICATOR


"""Create Conversion Functions"""


def convert_to_string(s):
    return str(s)


def convert_to_int(s):
    try:
        return int(s)
    except ValueError:
        raise ValueError(f"Value `{s}` cannot be cast to an int.")


def convert_to_float(s):
    try:
        return float(s)
    except ValueError:
        raise ValueError(f"Value `{s}` cannot be cast to a float.")

def convert_to_set(s):
    try:
        return {value for value in s}
    except ValueError:
        raise ValueError(f"Value `{s}` cannot be cast to a set.")

def convert_to_datetime(s):
    format_string = "%Y-%m-%d %H:%M:%S"
    try:
        return datetime.strptime(s, format_string)
    except ValueError:
        raise ValueError(f"Value `{s}` cannot be cast to a datetime")

def convert_to_date(s):
    format_string = "%Y-%m-%d"
    try:
        return datetime.strptime(s, format_string).date()
    except ValueError:
        raise ValueError(f"Value `{s}` cannot be cast to a date")

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

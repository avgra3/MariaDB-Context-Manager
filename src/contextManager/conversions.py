from datetime import date, datetime, time
from mariadb.constants import FIELD_TYPE

"""Create Conversion Functions"""
def convert_to_string(s):
    return str(s)

def convert_to_int(s):
    return int(s)

def convert_to_float(s):
    return float(s)

def convert_to_set(s):
    return {value for value in s}


def mariadb_to_python(value: int):
    if value in [FIELD_TYPE.VARCHAR, FIELD_TYPE.VAR_STRING, FIELD_TYPE.STRING]:
        return convert_to_string(value)
    if value in [FIELD_TYPE.TINY, FIELD_TYPE.LONGLONG, FIELD_TYPE.SHORT, FIELD_TYPE.LONG, FIELD_TYPE.INT24 ]:
        return convert_to_int(value)
    if value in [FIELD_TYPE.NEWDECIMAL, FIELD_TYPE.DECIMAL, FIELD_TYPE.FLOAT, FIELD_TYPE.DOUBLE]:
        return convert_to_float(value)
    if value in [FIELD_TYPE.SET]:
        return convert_to_set(value)
    if value in [FIELD_TYPE.DATE, FIELD_TYPE.NEWDATE, FIELD_TYPE.DATETIME2]:
        return date
    if value in [FIELD_TYPE.TIMESTAMP, FIELD_TYPE.TIME, FIELD_TYPE.TIMESTAMP2, FIELD_TYPE.TIME2]:
        return time
    if value in [FIELD_TYPE.DATETIME]:
        return datetime
    if value in [FIELD_TYPE.YEAR]:
        return date.year
    if value in [FIELD_TYPE.BIT, FIELD_TYPE.TINY_BLOB, FIELD_TYPE.MEDIUM_BLOB, FIELD_TYPE.BLOB]:
        return bytes
    if value in [FIELD_TYPE.JSON]:
        # This value returns JSON data
        return dict
    # Catches anything else and returns string
    return str

conversions = {
    ## **{FIELD_TYPE.TIME: timedelta_to_time},
    ## **{FIELD_TYPE.LONG: long_minus},
    ## **{FIELD_TYPE.NULL: none_to_string},
    ## **{FIELD_TYPE.LONGLONG: long_minus},
}
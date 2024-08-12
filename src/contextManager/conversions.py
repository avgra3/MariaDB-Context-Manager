from datetime import date, datetime, time
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

def none_to_mariadb_none(s):
    return INDICATOR.NULL

conversions = {
     **{FIELD_TYPE.LONG: convert_to_float},
     **{FIELD_TYPE.NULL: none_to_mariadb_none},
     **{FIELD_TYPE.LONGLONG: convert_to_float},
}

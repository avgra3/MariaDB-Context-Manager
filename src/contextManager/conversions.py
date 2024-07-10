from mariadb.constants import FIELD_TYPE
from datetime import datetime, date, time
import json

"""
    Need to add these later on:

    FIELD_TYPE.SET: func,
    FIELD_TYPE.BIT: func,
    FIELD_TYPE.LONG: func,
    FIELD_TYPE.TINY_BLOB: func,
    FIELD_TYPE.MEDIUM_BLOB: func,
    FIELD_TYPE.LONG_BLOB: func,
    FIELD_TYPE.GEOMETRY: func,
    FIELD_TYPE.TIME: func,
    FIELD_TYPE.TIME2: func,
    FIELD_TYPE.TIMESTAMP: func,
    FIELD_TYPE.TIMESTAMP2: func,
    FIELD_TYPE.BLOB: func,
    FIELD_TYPE.ENUM: func,
"""

def strings(string):
    return str(string)

def decimals(number):
    return float(number)

def integers(number):
    return int(number)

def floats(number):
    return float(number)

def handle_null(value):
    return None

def date_times(date):
    string_date = str(date)
    format = "%y-%m-%d %H:%M:%S"
    return datetime.strptime(string_date, format)

def dates(date):
    string_date = str(date)
    format = "%y-%m-%d"
    return datetime.strptime(string_date, format).date()

def jsons(json_object):
    return json.dump(json_object)

conversions = {
    FIELD_TYPE.DECIMAL: decimals,
    FIELD_TYPE.TINY: integers,
    FIELD_TYPE.SHORT: integers,    
    FIELD_TYPE.FLOAT: floats,
    FIELD_TYPE.DOUBLE: floats,
    FIELD_TYPE.NULL: handle_null,
    FIELD_TYPE.INT24: integers,
    FIELD_TYPE.DATE: dates,
    FIELD_TYPE.LONGLONG: integers,
    FIELD_TYPE.DATETIME: date_times,
    FIELD_TYPE.YEAR: integers,
    FIELD_TYPE.NEWDATE: dates,
    FIELD_TYPE.VARCHAR: strings,
    FIELD_TYPE.DATETIME2: date_times,
    FIELD_TYPE.JSON: jsons,
    FIELD_TYPE.NEWDECIMAL: decimals,
    FIELD_TYPE.VAR_STRING: integers,
    FIELD_TYPE.STRING: integers,
}
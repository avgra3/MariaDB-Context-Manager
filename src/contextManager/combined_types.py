from mariadb.constants import FIELD_TYPE
from typing import List, Dict


def convert_to_python(value) -> str:
    if (
        value == FIELD_TYPE.DECIMAL
        or value == FIELD_TYPE.FLOAT
        or value == FIELD_TYPE.DOUBLE
        or value == FIELD_TYPE.NEWDECIMAL
    ):
        return "float"
    if (
        value == FIELD_TYPE.INT24
        or value == FIELD_TYPE.TINY
        or value == FIELD_TYPE.SHORT
        or value == FIELD_TYPE.LONG
        or value == FIELD_TYPE.LONGLONG
        or value == FIELD_TYPE.YEAR
    ):
        return "int"
    if (
        value == FIELD_TYPE.VAR_STRING
        or value == FIELD_TYPE.STRING
        or value == FIELD_TYPE.VARCHAR
    ):
        return "str"
    if (
        value == FIELD_TYPE.TIMESTAMP
        or value == FIELD_TYPE.TIMESTAMP2
    ):
        return "timestamp"
    if (
        value == FIELD_TYPE.TIME
        or value == FIELD_TYPE.TIME2
    ):
        return "time"
    if (
        value == FIELD_TYPE.DATETIME
        or value == FIELD_TYPE.DATETIME2
    ):
        return "datetime"
    if (
        value == FIELD_TYPE.DATE
        or value == FIELD_TYPE.NEWDATE
    ):
        return "date"
    return "str"


def make_type_dictionary(
    column_names: List[str], mariadb_data_types: List[str]
) -> Dict[str, str]:
    values = list(map(convert_to_python, mariadb_data_types))
    return {
        column_names: mariadb_data_types
        for column_names, mariadb_data_types in zip(column_names, values)
    }

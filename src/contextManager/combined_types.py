from mariadb.constants import FIELD_TYPE

def convert(value) -> str:
    if value == FIELD_TYPE.DECIMAL or value == FIELD_TYPE.FLOAT or value == FIELD_TYPE.DOUBLE or value == FIELD_TYPE.NEWDECIMAL:
        return "float"
    elif value == FIELD_TYPE.INT24 or value == FIELD_TYPE.TINY or value == FIELD_TYPE.SHORT or value == FIELD_TYPE.LONG or value == FIELD_TYPE.LONGLONG:
        return "int"
    elif value == FIELD_TYPE.VAR_STRING or value == FIELD_TYPE.STRING or value == FIELD_TYPE.VARCHAR:
        return "str"
    elif value == FIELD_TYPE.DATE or value == FIELD_TYPE.TIME or value == FIELD_TYPE.DATETIME or value == FIELD_TYPE.YEAR or value == FIELD_TYPE.TIMESTAMP or value == FIELD_TYPE.NEWDATE or value == FIELD_TYPE.TIMESTAMP2 or value == FIELD_TYPE.DATETIME2 or value == FIELD_TYPE.TIME2:
        return "str"
    else:
        return "str"

def make_type_dictionary(column_names: list[str], data_types: list[str]) -> dict:
    values = list(map(convert, data_types))
    return {column_names: data_types for column_names, data_types in zip(column_names, values)}
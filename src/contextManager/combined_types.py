from mariadb.constants import FIELD_TYPE

def convert(raw_list: list[int]) -> list[str]:
    converted_list = []
    for value in raw_list:
        if value in [FIELD_TYPE.DECIMAL, FIELD_TYPE.FLOAT, FIELD_TYPE.DOUBLE, FIELD_TYPE.NEWDECIMAL]:
            converted_list.append("float")
        if value in [FIELD_TYPE.INT24, FIELD_TYPE.TINY, FIELD_TYPE.SHORT, FIELD_TYPE.LONG, FIELD_TYPE.LONGLONG]:
            converted_list.append("int")
        if value in [FIELD_TYPE.VAR_STRING, FIELD_TYPE.STRING, FIELD_TYPE.VARCHAR]:
            converted_list.append("str")
        if value in [FIELD_TYPE.DATE, FIELD_TYPE.TIME, FIELD_TYPE.DATETIME, FIELD_TYPE.YEAR, FIELD_TYPE.TIMESTAMP, FIELD_TYPE.NEWDATE, FIELD_TYPE.TIMESTAMP2, FIELD_TYPE.DATETIME2, FIELD_TYPE.TIME2]:
            converted_list.append("str")
        # TODO: Implement the Python equivalents of these:
        if value == FIELD_TYPE.NULL:
            pass
        if value == FIELD_TYPE.BIT:
            pass
        if value == FIELD_TYPE.JSON:
            pass
        if value == FIELD_TYPE.ENUM:
            pass
        if value == FIELD_TYPE.SET:
            pass
        if value == FIELD_TYPE.TINY_BLOB:
            pass
        if value == FIELD_TYPE.MEDIUM_BLOB:
            pass
        if value == FIELD_TYPE.LONG_BLOB:
            pass
        if value == FIELD_TYPE.BLOB:
            pass
        if value == FIELD_TYPE.GEOMETRY:
            pass
        else:
            converted_list.append("str")

    return converted_list


def make_type_dictionary(column_names: list[str], data_types: list[str]) -> dict:
    return {column_names[i]: data_types[i] for i in range(len(column_names))}
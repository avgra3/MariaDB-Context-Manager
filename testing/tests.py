import unittest
from datetime import date, datetime, time
from ..src.contextManager.conversions import mariadb_to_python
from ..src.contextManager.contextManager import MariaDBCM


class TestConversions(unittest.TestCase):
    def test_string_conversion_success(self):
        string_list = [15, 253, 254]
        for i in string_list:
            assert mariadb_to_python(value=i) == str

    def test_int_conversion_success(self):
        int_list = [8, 1, 2, 3, 8, 9]
        for i in int_list:
            assert mariadb_to_python(value=i) == int

    def test_float_conversion_success(self):
        float_list = [246, 0, 4, 5]
        for i in float_list:
            assert mariadb_to_python(value=i) == float

    def test_set_conversion_success(self):
        set_list = [248]
        for i in set_list:
            assert mariadb_to_python(value=i) == set

    def test_date_conversion_success(self):
        date_list = [10, 14, 18]
        for i in date_list:
            assert mariadb_to_python(value=i) == date

    def test_time_conversion_success(self):
        time_list = [7, 11, 17, 19]
        for i in time_list:
            assert mariadb_to_python(value=i) == time

    def test_datetime_conversion_success(self):
        datetime_list = [12]
        for i in datetime_list:
            assert mariadb_to_python(value=i) == datetime

    def test_year_conversion_success(self):
        year_list = [13]
        for i in year_list:
            assert mariadb_to_python(value=i) == date.year

    def test_bytes_conversion_success(self):
        bytes_list = [16, 249, 250, 251, 252]
        for i in bytes_list:
            assert mariadb_to_python(value=i) == bytes

    def test_json_conversion_success(self):
        json_list = [245]
        for i in json_list:
            assert mariadb_to_python(value=i) == dict


class TestMariaDBCM(unittest.TestCase):
    pass


if __name__ == "__main__":
    unittest.main()

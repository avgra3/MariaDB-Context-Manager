import unittest

from src.mariadb_context_manager.conversions import (
        convert_to_string,
        convert_to_int,
        convert_to_float, 
        convert_to_set,
)

class TestConversions(unittest.TestCase):
    def test_convert_to_string(self):
        input = "this should be a string"
        result = convert_to_string(input)
        self.assertIsInstance(result, str, f"Should be a string. Is of type `{type(result)}`")

    def test_convert_to_int(self):
        input = 1.0
        result = convert_to_int(input)
        self.assertIsInstance(result, int, "Should be a string. Is of type `{type(result)}`")

    def test_convert_to_int_fails(self):
        input = "This is not a number"
        with self.assertRaises(ValueError):
            result = convert_to_int(input)

    def test_convert_to_float(self):
        input = 1
        result = convert_to_float(input)
        self.assertIsInstance(result, float, "Should be a float. Is of type `{type(result)}`")

    def test_convert_to_float_fails(self):
        input = "this should fail"
        with self.assertRaises(ValueError):
            result = convert_to_int(input)

    def test_convert_to_set(self):
        input = (1, 2, 3)
        result = convert_to_set(input)
        self.assertIsInstance(result, set, "Should be a set. Is of type `{type(result)}`")

if __name__ == "__main__":
    unittest.main()

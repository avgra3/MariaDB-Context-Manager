import unittest
from src.mariadb_context_manager.contextManager import MariaDBResult

MOCK_DB_CONNECTIONS = {
        "user": "test",
        "password": "test",
        "host": "localhost",
        "database": "test",
}

SQL_SINGLE_RESULT = "SELECT 1, 'test';"
EXPECTED_SQL_RESULT = MariaDBResult(
    metadata =  {"test": "test"},
    result = [(1, "test")],
)

class TestMariaDBCM(unittest.TestCase):
    def test_run_sql(self):
       pass


if __name__ == "__main__":
    unittest.main()


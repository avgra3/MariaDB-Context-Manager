import unittest
from unittest.mock import patch, MagicMock
from src.mariadb_context_manager.contextManager import MariaDBResult, MariaDBCM

MOCK_DB_CONNECTIONS = {
        "user": "test",
        "password": "test",
        "host": "localhost",
        "database": "test",
}

SQL_SINGLE_RESULT = "SELECT 1, 'test';"
EXPECTED_SQL_RESULT = MariaDBResult(
    metadata =  {"test", "test"},
    result = [(1, "test")],
)

class TestMariaDBCM(unittest.TestCase):
    @patch("src.mariadb_context_manager.contextManager.mariadb.ConnectionPool")
    def test_run_sql(self, mock_connect):
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [(1, "test")]
        mock_connect.return_value.cursor.return_value.__enter__.return_value = mock_cursor
        dbManager = MariaDBCM(logger=None, **MOCK_DB_CONNECTIONS)
        run_sql = dbManager.run_sql(SQL_SINGLE_RESULT)
        self.assertEqual(run_sql, EXPECTED_SQL_RESULT.result)
        mock_connect.assert_called_once_with(MOCK_DB_CONNECTIONS)
        mock_cursor.execute.assert_called_once_with(SQL_SINGLE_RESULT)


if __name__ == "__main__":
    unittest.main()


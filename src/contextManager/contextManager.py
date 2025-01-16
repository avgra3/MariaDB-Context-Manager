import mariadb
from .conversions import conversions
from .combined_types import make_type_dictionary


# This will implement a context manager to work with MariaDB
class MariaDBCM:
    def __init__(
        self,
        host: str,
        user: str,
        password: str,
        database: str,
        port: int,
        buffered: bool = True,
        # Add functionality for converter
        converter: dict = None,
        return_dict: bool = False,
        prepared: bool = False,
        # Allows for loading infile
        allow_load_infile: bool = False,
    ):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.database = database
        self.buffered = buffered
        self.allow_load_infile = allow_load_infile
        # Makes our connection to mariadb
        self.conn = mariadb.connect(user=self.user,
                                    password=self.password,
                                    host=self.host,
                                    port=self.port,
                                    database=self.database,
                                    local_infile=self.allow_load_infile)
        self.cur = self.conn.cursor()

    def __enter__(self):
        print(f"Connection to {self.database} was made")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.close()
        print('\nConnection has been closed...\n')
        if exc_type:
            print(f"exc_type: {exc_type}")
            print(f"exc_value: {exc_value}")
            print(f"traceback: {traceback}")
        return self

    def __check_connection_open(self) -> bool:
        if self.conn.cursor().closed:
            return False
        return True

    def __remove_comments(self, query: str) -> str:
        updated_query = ""
        for line in query.splitlines():
            if not (line.strip()).startswith("--"):
                updated_query += line.strip()

    def execute_change(self, statement: str, parameters: tuple) -> dict:
        if statement.strip() != "" and parameters is not None:
            ran_statement = self.cur.execute_many(statement, parameters)
            statement_results = {"statement": ran_statement.statement,
                                 "rows_updated": ran_statement.rowcount,
                                 "number_of_warnings": ran_statement.warnings}
            return statement_results

    def execute(self, query: str) -> dict:
        result = {}
        if query.strip() != "":
            with self.conn as conn:
                cursor = conn.cursor(
                    dictionary=self.return_dict, prepared=self.prepared
                )
                cursor.execute(query)
                metadata = cursor.metadata
                if cursor.rowcount >= 0 and cursor.description:
                    result["data"] = cursor.fetchall()
                result["columns"] = metadata["field"]
                result["statement_ran"] = cursor.statement
                result["warnings"] = cursor.warnings
                result["rowcount"] = cursor.rowcount
                result["data_types"] = make_type_dictionary(
                    column_names=result["columns"], data_types=result["types"])
        else:
            print("No query given")

        return result

    def execute_many(self, queries: str) -> list:
        results = []
        for query in queries.strip().split(";"):
            result = self.execute(query)
            results.append(result)
        return results

    def execute_stored_procedure(self, stored_procedure_name: str, inputs: tuple = ()):
        with self.conn as conn:
            cursor = conn.cursor(
                dictionary=self.return_dict, prepared=self.prepared)
            cursor.callproc(stored_procedure_name, inputs)
            result = {}
            metadata = cursor.metadata
            if cursor.sp_outparams:
                result["data"] = cursor.fetchall()
            result["columns"] = metadata["field"]
            result["warnings"] = cursor.warnings
            result["rowcount"] = cursor.rowcount
            result["data_types"] = make_type_dictionary(
                column_names=result["columns"], data_types=result["types"])
        return result

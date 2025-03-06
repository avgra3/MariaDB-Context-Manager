import mariadb
from .conversions import conversions
from .combined_types import make_type_dictionary
import logging


class MariaDBCM:
    __slots__ = ("host", "user", "password", "database", "port", "buffered",
                 "converter", "return_dict", "prepared", "allow_local_infile",
                 "conn", "cur")

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
        self.conn = mariadb.connect(
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.database,
            local_infile=self.allow_load_infile,
            converter=conversions,
        )

    def __enter__(self):
        '''Information that there was a successful connection to the database.'''
        logging.info(f"Connection to {self.database} was made")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        '''Upon exit, the connection to the database is closed.'''
        self.conn.close()
        logging.info("\nConnection has been closed...\n")
        if exc_type:
            logging.error(f"exc_type: {exc_type}")
            logging.error(f"exc_value: {exc_value}")
            logging.error(f"traceback: {traceback}")
        return self

    def __check_connection_open(self) -> bool:
        """Checks that the connection to the database is open.
        Returns False if the connection is closed, otherwise open."""
        if self.conn.cursor().closed:
            return False
        return True

    def __remove_comments(self, query: str) -> str:
        """Removes comments from a given query
        query: str, the SQL statement that is used."""
        updated_query = ""
        for line in query.splitlines():
            if not (line.strip()).startswith("--"):
                updated_query += line.strip()

    def execute_change(
        self, statement: str, parameters: tuple
    ) -> dict[str, any]:
        '''statement: The SQL update script
        parameters: that are used in the update.
        Returns a dictionary of information from results of changes.'''
        self.make_cursor()
        if statement.strip() != "" and parameters is not None:
            ran_statement = self.cur.execute_many(statement, parameters)
            statement_results = {
                "statement": ran_statement.statement,
                "rows_updated": ran_statement.rowcount,
                "number_of_warnings": ran_statement.warnings,
            }
            return statement_results
        return {}

    def execute(self, query: str) -> dict[dict, any]:
        '''Execute a SQL query. This can be used for
        updates, deletes, inserts which do not need parameters.
        query: str which contains the SQL query ran.'''
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
                    column_names=result["columns"], data_types=result["types"]
                )
        else:
            print("No query given")

        return result

    def execute_many(self, queries: str) -> list[dict[str, any]]:
        '''Similar to execute but allows for many queries to be ran
        sequentially.
        Note: This is not a sophisticated query execution and expects that
        all queries are delimited by a ";", and there are no semicolons
        used within queries.
        queries: str, run many queries.
        Returns a list of dictionaries from the execute method.'''
        results = []
        for query in queries.strip().split(";"):
            result = self.execute(query)
            results.append(result)
        return results

    def execute_stored_procedure(
        self, stored_procedure_name: str, inputs: tuple = (),
    ) -> dict[str, any]:
        '''Execution of stored procedures.
        stored_procedure_name: str, the name of the stored procedure.
        inputs: tuple, all inputs that would be needed for the given
            stored procedure.
        Note: this assumes the stored procedure exists and the user
            knows the needed parameters.
        Returns a dictionary similar to execute.'''
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
                column_names=result["columns"], data_types=result["types"]
            )
        return result

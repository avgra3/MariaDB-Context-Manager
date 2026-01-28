import mariadb
from .conversions import conversions
from .combined_types import make_type_dictionary
from .constants import LOGGER
from logging import Logger

class MariaDBCM:
    __slots__ = (
        "host",
        "user",
        "password",
        "database",
        "port",
        "buffered",
        "converter",
        "return_dict",
        "prepared",
        "allow_local_infile",
        "conn",
        "cur",
    )

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
        allow_local_infile: bool = False,
        # Allows for user's own logger or to use the default one
        logger: Logger = LOGGER
    ):
        self.user: str = user
        self.password: str = password
        self.host: str = host
        self.port: int = port
        self.database: str = database
        self.buffered: bool = buffered
        self.allow_local_infile: bool = allow_local_infile
        self.return_dict: dict = return_dict
        self.prepared: bool = prepared
        # Makes our connection to mariadb
        self.conn = mariadb.connect(
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.database,
            local_infile=self.allow_local_infile,
            converter=conversions,
        )
        self.logger: Logger = logger

    def __new_conn(self):
        if not self.__check_connection_open():
            self.logger.info("Connection closed. Reopening...")
            self.conn = mariadb.connect(
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
                database=self.database,
                local_infile=self.allow_local_infile,
                converter=conversions,
            )
            if self.__check_connection_open():
                self.logger.info("Connection opened succesffully!")
                return
            self.logger.warning("Connection did not open...")

    def __enter__(self):
        """
        Information that there was a successful connection to the database.
        """
        self.logger.info(f"Connection to {self.database} was made")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Upon exit, the connection to the database is closed."""
        if self.conn.open:
            # self.
            self.logger.info("Closing connection...")
            self.conn.close()
        # self.
        self.logger.info("\nConnection has been closed...\n")
        if exc_type:
            self.logger.error(f"exc_type: {exc_type}")
            self.logger.error(f"exc_value: {exc_value}")
            self.logger.error(f"traceback: {traceback}")
        return self

    def __check_connection_open(self) -> bool:
        """Checks that the connection to the database is open.
        Returns False if the connection is closed, otherwise open."""
        try:
            self.conn.open
            return True
        except Exception:
            self.logger.warning("Connection is closed...")
        return False

    def __remove_comments(self, query: str) -> str:
        """Removes comments from a given query
        query: str, the SQL statement that is used."""
        updated_query = ""
        for line in query.splitlines():
            if not (line.strip()).startswith("--"):
                updated_query += line.strip()
        return updated_query

    def execute_change(
        self, statement: str = "", parameters: list[tuple, ...] = None
    ) -> dict[str, any]:
        """statement: The SQL update script
        parameters: that are used in the update.
        Returns a dictionary of information from results of changes."""
        if statement.strip() == "":
            self.logger.warning("SQL statement used was empty...")
            return {}
        if parameters is None:
            self.logger.warning("No parameters were used...")
            return {}
        self.__new_conn()
        with self.conn as conn:
            cur = conn.cursor(
                **{
                    "dictionary": self.return_dict,
                    "prepared": self.prepared,
                }
            )
            if (
                statement.strip() != ""
                and statement is not None
                and isinstance(statement, str)
                and parameters is not None
                and isinstance(parameters, list)
                and isinstance(parameters[0], tuple)
                and len(parameters) >= 1
                and len(parameters[0]) >= 1
            ):
                cur.executemany(statement, parameters)
                warnings = self.conn.show_warnings() if cur.warnings > 0 else ""
                statement_results = {
                    "statement": cur.statement,
                    "rows_updated": cur.rowcount,
                    "number_of_warnings": cur.warnings,
                    "warnings": warnings,
                }
                return statement_results

    def execute(self, query: str) -> dict[dict, any]:
        """Execute a SQL query. This can be used for
        updates, deletes, inserts which do not need parameters.
        query: str which contains the SQL query ran."""
        result = {}
        self.__new_conn()
        if query.strip() != "":
            with self.conn as conn:
                cursor = conn.cursor(
                    **{
                        "dictionary": self.return_dict,
                        "prepared": self.prepared,
                    }
                )
                cursor.execute(query)
                metadata = cursor.metadata
                if metadata is not None:
                    if cursor.rowcount >= 0 and cursor.description:
                        result["data"] = cursor.fetchall()
                    if metadata["field"] is not None:
                        result["columns"] = metadata["field"]
                        result["data_types"] = make_type_dictionary(
                            column_names=result["columns"],
                            mariadb_data_types=metadata["type"],
                        )
                    result["statement_ran"] = cursor.statement
                    result["warnings"] = cursor.warnings
                    result["rowcount"] = cursor.rowcount

        else:
            self.logger.warning(f"""
            No query was given...
            Query received: \"{query}\
            """)
        return result

    def execute_many(self, queries: str) -> list[dict[str, any]]:
        """Similar to execute but allows for many queries to be ran
        sequentially.
        Note: This is not a sophisticated query execution and expects that
        all queries are delimited by a ";", and there are no semicolons
        used within queries.
        queries: str, run many queries.
        Returns a list of dictionaries from the execute method."""
        results = []
        for query in queries.strip().split(";"):
            if query.strip() != "":
                result = self.execute(query)
                results.append(result)
        return results

    def execute_stored_procedure(
        self, stored_procedure_name: str, inputs: tuple = (),
    ) -> dict[str, any]:
        """
        Execution of stored procedures.
        stored_procedure_name: str, the name of the stored procedure.
        inputs: tuple, all inputs that would be needed for the given
            stored procedure.
        Note: this assumes the stored procedure exists and the user
            knows the needed parameters.
        Returns a dictionary similar to execute.
        """
        self.__new_conn()
        result = {}
        self.logger.info(f"Current conn: {self.conn}")
        with self.conn as conn:
            cursor = conn.cursor()
            cursor.callproc(stored_procedure_name, inputs)
            metadata = cursor.metadata
            if cursor.sp_outparams:
                result["data"] = cursor.fetchall()
            result["columns"] = metadata["field"]
            result["warnings"] = cursor.warnings
            result["rowcount"] = cursor.rowcount
            result["data_types"] = make_type_dictionary(
                column_names=result["columns"],
                mariadb_data_types=metadata["type"],
            )
        return result

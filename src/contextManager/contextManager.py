import mariadb
from .conversions import conversions
from .combined_types import make_type_dictionary
import logging

# Logger format
# FORMAT = "%(asctime)s %(clientip)-15s %(user)-8s %(message)s"
# logging.basicConfig(format=FORMAT)
# logger = logging.getLogger()


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
        allow_local_infile: bool = False,
    ):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.database = database
        self.buffered = buffered
        self.allow_local_infile = allow_local_infile
        self.return_dict = return_dict
        self.prepared = prepared
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
        # Logger format
        FORMAT = "{asctime} - {levelname} - {message}"
        logging.basicConfig(
            format=FORMAT,
            style="{",
            datefmt="%Y-%m-%d %H:%M",
        )

    def __new_con(self):
        if not self.__check_connection_open():
            logging.info("Connection closed. Reopening...")
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
                logging.info("Connection opened succesffully!")
                return
            logging.warning("Connection did not open...")

    def __enter__(self):
        '''Information that there was a successful connection to the database.'''
        logging.info(f"Connection to {self.database} was made")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        '''Upon exit, the connection to the database is closed.'''
        if self.conn.open:
            self.logger.info("Closing connection...")
            self.conn.close()
        self.logger.info("\nConnection has been closed...\n")
        if exc_type:
            logging.error(f"exc_type: {exc_type}")
            logging.error(f"exc_value: {exc_value}")
            logging.error(f"traceback: {traceback}")
        return self

    def __check_connection_open(self) -> bool:
        """Checks that the connection to the database is open.
        Returns False if the connection is closed, otherwise open."""
        try:
            self.conn.open
            return True
        except Exception:
            logging.warning("Connection is closed...")
        return False

    def __remove_comments(self, query: str) -> str:
        """Removes comments from a given query
        query: str, the SQL statement that is used."""
        updated_query = ""
        for line in query.splitlines():
            if not (line.strip()).startswith("--"):
                updated_query += line.strip()

    def execute_change(
        self, statement: str, parameters: list[tuple, ...]
    ) -> dict[str, any]:
        '''statement: The SQL update script
        parameters: that are used in the update.
        Returns a dictionary of information from results of changes.'''
        if statement.strip() == "" or statement is None or parameters is None:
            if statement.strip() == "" or statement is None:
                logging.warning("SQL statement used was empty")
            if parameters is None:
                logging.warning("No parameters were useed")
            return {}
        self.__new_con()
        with self.conn as conn:
            cur = conn.cursor(
                **{
                    "dictionary": self.return_dict,
                    "prepared": self.prepared,
                }
            )
            if (
                statement.strip() != "" and
                statement is not None and
                isinstance(statement, str) and
                parameters is not None and
                isinstance(parameters, list) and
                isinstance(parameters[0], tuple) and
                len(parameters) >= 1 and
                len(parameters[0]) >= 1
            ):
                cur.executemany(statement, parameters)
                statement_results = {
                    "statement": cur.statement,
                    "rows_updated": cur.rowcount,
                    "number_of_warnings": cur.warnings,
                    "warnings": self.conn.show_warnings() if cur.warnings > 0 else "",
                }
                return statement_results

    def execute(self, query: str) -> dict[dict, any]:
        '''Execute a SQL query. This can be used for
        updates, deletes, inserts which do not need parameters.
        query: str which contains the SQL query ran.'''
        result = {}
        self.__new_con()
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
            logging.warning(f"No query was given. {query}")
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

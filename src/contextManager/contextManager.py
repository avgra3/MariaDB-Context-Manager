import mariadb


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
        allow_local_infile: bool = False,
    ):
        print('Initializing connection...\n')
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.database = database
        self.buffered = buffered
        self.allow_load_infile = allow_local_infile
        # Makes our connection to mariadb
        self.conn = mariadb.connect(user=self.user,
                                    password=self.password,
                                    host=self.host,
                                    port=self.port,
                                    database=self.database
                                    local_infile=self.allow_load_infile)
        self.cur = self.conn.cursor()

    def __enter__(self):
        print(f"Connection to {self.database} was made")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.close()
        print('\nConnection has been closed...\n')
        if exc_type:
            print(f'exc_type: {exc_type}')
            print(f'exc_value: {exc_value}')
            print(f'traceback: {traceback}')
        return True

    def __remove_comments(self, query: str) -> str:
        updated_query = ""
        for line in query.splitlines():
            if not (line.strip()).startswith("--"):
                updated_query += line.strip()

    def __execute_query(self, query: str) -> dict:
        ran_query = self.cur.execute(query, buffered=self.buffered)
        query_results = {"statement": ran_query.statement,
                         "rows_updated": ran_query.rowcount,
                         "number_of_warnings": ran_query.warnings}
        return query_results

    def execute(self, queries: str) -> list:
        query_list = (self.__remove_comments(queries)).split(";")
        query_results = []
        for query in query_list:
            if query.strip() != "":
                query_results.append(self.__execute_query(query))
        return query_results

    def execute_change(self, statement: str, parameters: tuple) -> dict:
        if statement.strip() != "" and parameters is not None:
            ran_statement = self.cur.execute_many(statement, parameters)
            statement_results = {"statement": ran_statement.statement,
                                 "rows_updated": ran_statement.rowcount,
                                 "number_of_warnings": ran_statement.warnings}
            return statement_results

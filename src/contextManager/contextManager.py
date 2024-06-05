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
        return_dict: bool = False,
        prepared: bool = False,
        # Allows for loading infile
        allow_load_infile: bool = False,
    ):
        print("Initializing connection...\n")
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.database = database
        self.return_dict = return_dict
        self.prepared = prepared
        self.allow_load_infile = allow_load_infile
        # Makes our connection to mariadb
        self.conn = mariadb.connect(
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.database,
            local_infile=self.allow_load_infile,
        )
        self.cur = self.conn.cursor(
            dictionary=self.return_dict,
            prepared=self.prepared,
        )

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.close()
        print(f"\nConnection has been closed...\n")
        if exc_type:
            print(f"exc_type: {exc_type}")
            print(f"exc_value: {exc_value}")
            print(f"traceback: {traceback}")
        return True

    def __check_connection_open(self) -> bool:
        if self.cur.closed:
            return False
        return True

    def execute(self, query: str) -> dict:
        result = {}
        cols = []
        if query.strip() != "":
            with self.conn as conn:
                self.cur.execute(query)
                if self.cur.description:
                    for item in list(self.cur.description):
                        cols.append(item[0])
                result["columns"] = cols
                result["statement_ran"] = self.cur.statement
                result["warnings"] = self.cur.warnings
                if self.cur.rowcount > 0 and self.cur.description:
                    result["data"] = self.cur.fetchall()
        else:
            print("No query given")
        self.cur.close()
        return result

    def execute_many(self, queries: str) -> list:
        results = []
        for query in queries.strip().split(";"):
            if not self.__check_connection_open():
                self.conn = mariadb.connect(
                    user=self.user,
                    password=self.password,
                    host=self.host,
                    port=self.port,
                    database=self.database,
                    local_infile=self.allow_load_infile,
                )
                self.cur = self.conn.cursor(
                    dictionary=self.return_dict, prepared=self.prepared
                )
            result = self.execute(query)
            results.append(result)
        return results

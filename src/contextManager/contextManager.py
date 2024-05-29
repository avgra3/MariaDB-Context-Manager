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
    ):
        print("Initializing connection...\n")
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.database = database
        self.return_dict = return_dict
        self.prepared = prepared
        # Makes our connection to mariadb
        self.conn = mariadb.connect(
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.database,
            dictionary=self.return_dict,
            prepared=self.prepared,
        )
        self.cur = self.conn.cursor()

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

    def execute(self, query: str) -> dict:
        result = {}
        cols = []
        with self.conn as conn:
            self.cur.execute(query.strip())
            for item in list(self.cur.description):
                cols.append(item[0])
            result["columns"] = cols
            result["statement_ran"] = self.cur.statement
            result["warnings"] = self.cur.warnings
            if self.cur.rowcount > 0:
                result["data"] = self.cur.fetchall()
            self.cur.close()
        return result
    
    def execute_many(self, queries: str) -> list:
        results = []
        for query in queries.split(";"):
            result = self.execute(query=query)
            results.append(result)
        return results
        

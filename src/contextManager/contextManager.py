import mariadb
from .conversions import conversions
from .constants import LOGGER
from logging import Logger
from dataclasses import dataclass
from pathlib import Path
import subprocess
import sys

@dataclass
class MariaDBResult:
    metadata: dict
    result: list[tuple] | None = None
    warning_count: int = 0
    warnings: list[str] | None = None
    query: str | None = None

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
        self.pool_size: int = pool_size
        self.pool_name: str = (
                "mariadb_runner" + f"_{pool_name}"
                if pool_name is not None and pool_name != ""
            else ""
        )
        # Makes our connection to mariadb
        self.dbCons = {
            "user": self.user,
            "password": self.password,
            "host": self.host, 
            "port": self.port,
            "database": self.database,
            "local_infile": self.allow_local_infile,
            "pool_size": self.pool_size,
            "pool_reset_connection": True, 
            "pool_name": self.pool_name, 
            "converter": conversions,
        }
        self.pool = self._create_pool(**self.dbCons)
        self.logger.er: Logger = logger

    def _create_pool(self):
        return mariadb.ConnectionPool(**self.dbCons)

    def run_direct_sql(self, sql: Path) -> MariaDBResult:
        temp_password = (
            self.dbCons["password"]
            if self.dbCons["password"] == "forget1c"
            else "forget1c"
        )
        with open(sql, "r") as f:
            try:
                result = subprocess.run(
                    [
                        "mariadb",
                        f"--user={self.dbCons['user']}",
                        f"--password={temp_password}",
                        f"--host={self.dbCons['host']}",
                        f"--port={self.dbCons['port']}",
                        "--show-warnings",
                        "-v",
                        "-v",
                        "-v",
                        self.dbCons["database"],
                    ],
                    capture_output=True,
                    text=True,
                    stdin=f,
                    check=True,
                )
            except subprocess.CalledProcessError as e:
                self.logger.critical(f"Exception raised: {e}")
                sys.exit(-1)
        self.logger.info(result.stdout)
        if result.stderr is not None:
            self.logger.error(result.stderr)
        mariaResult = MariaDBResult(
            metadata={"direct_run": None},
            result=[(result.stdout, result.stderr)],
            query=sql.read_text(),
        )
        return mariaResult

    def run_sql(self, sql_queries: list[str]) -> list[MariaDBResult]:
        results: list[MariaDBResult] = []
        try:
            for sql in sql_queries:
                with self.pool.get_connection() as conn:
                    self.logger.info(f"Running sql script: {sql}")
                    cur = conn.cursor()
                    cur.execute(statement=sql)
                    rowcount = cur.rowcount
                    result = None
                    meta = cur.metadata
                    self.logger.info(f"Updated/Retrieved {rowcount:,} rows")
                    if cur.warnings > 0:
                        warning_count = cur.warnings
                        warnings = conn.show_warnings()
                        self.logger.warning(warnings)
                    else:
                        warning_count = 0
                        warnings = None
                    results.append(
                        MariaDBResult(
                            result=result,
                            metadata=meta,
                            warning_count=warning_count,
                            warnings=warnings,
                        )
                    )
                    cur.close()
        except mariadb.ProgrammingError as e:
            error_message: str = f"ProgrammingError => {e}"
            self.logger.error(error_message)
            sys.exit(-1)

        except mariadb.Error as e:
            error_message: str = (
                f"""An error occured while running the previous sql.
                Review error message for details => {e}"""
            )
            self.logger.error(error_message)
            sys.exit(-1)
        self.pool.close()
        return results

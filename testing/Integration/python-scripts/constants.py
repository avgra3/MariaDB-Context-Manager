from os import getenv

# Database connection parameters
user = getenv("MARIADB_USER")
password = getenv("MARIADB_PASSWORD")
host = getenv("MARIADB_HOST")
port = getenv("MARIADB_PORT")
database = getenv("MARIADB_DB")
connectionParams = {
    "user": user,
    "password": password,
    "host": host,
    "port": port,
    "database": database,
}

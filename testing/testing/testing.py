from pathlib import Path
import importlib.util as importer


# Importing Local package
spec = importer.spec_from_file_location("context-manager", str(Path("../contextManager/contextManager.py").resolve()))
mariadb_context_manager = importer.module_from_spec(spec)
spec.loader.exec_module(mariadb_context_manager)


# Get Current Config
# Database connection parameters
user = "testUser"
password = "testUserPassword"
host = "192.168.92.22"
port = 3306
database = "testDB"
connectionParams = {
    "user": user,
    "password": password,
    "host": host,
    "port": port,
    "database": database,
}



# Test We can Connect
def test_connect():
    # connection = mariadb_context_manager.MariaDBCM(**config)
    test_query = "SHOW PROCESSLIST;"
    # results = connection.execute(test_query)
    #results = mariadb_context_manager.MariaDBCM(**config).execute(test_query)
    #for item in results:
    #    print(item)

    with mariadb_context_manager.MariaDBCM(**connectionParams) as con:
        result = con.execute(test_query)
        for r in result:
            print(r)


def main():
    test_connect()


if __name__ == "__main__":
    main()

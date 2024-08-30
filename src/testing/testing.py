from pathlib import Path
import toml
import importlib.util as importer


# Importing Local package
spec = importer.spec_from_file_location("context-manager", str(Path("../contextManager/contextManager.py").resolve()))
mariadb_context_manager = importer.module_from_spec(spec)
spec.loader.exec_module(mariadb_context_manager)


# Get Current Config
def get_configuration() -> dict[str, any]:
    # Load in configuration
    with open("config.toml", "r") as config:
        configuration = toml.load(config)
    mariadb_conn_params: dict[str, any] = {"user": configuration["database"]["username"], "password": configuration["database"]["password"], "host": configuration["server"]["host"], "port": configuration["server"]["port"], "database": configuration["database"]["database"]}
    return mariadb_conn_params


config = get_configuration()


# Test We can Connect
def test_connect():
    # connection = mariadb_context_manager.MariaDBCM(**config)
    test_query = "SHOW PROCESSLIST;"
    # results = connection.execute(test_query)
    #results = mariadb_context_manager.MariaDBCM(**config).execute(test_query)
    #for item in results:
    #    print(item)

    with mariadb_context_manager.MariaDBCM(**config) as con:
        result = con.execute(test_query)
        for r in result:
            print(r)


def main():
    test_connect()


if __name__ == "__main__":
    main()

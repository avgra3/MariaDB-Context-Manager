from pathlib import Path
import toml

# Importing Local package
spec = importer.spec_from_file_location("context-manager", str(Path("../context-manager/context-manager.py").resolve()))
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
    connection = mariadb_context_manager.MariaDBCM(**self.mariadb_conn_params)
    test_query = "SHOW PROCESSLIST;"
    results = connection.execute(connection)
    for item in results:
        print(item)

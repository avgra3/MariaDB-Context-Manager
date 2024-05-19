import mariadb

# This will implement a context manager to work with MariaDB
class MariaDBCM:
    def __init__(self, host: str, user: str, password: str, database: str, port: int):
        print('Initializing connection...\n')
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.database = database
        # Makes our connection to mariadb
        self.conn = mariadb.connect(user=self.user,
                               password=self.password,
                               host=self.host,
                               port=self.port,
                               database=self.database)
        self.cur = self.conn.cursor()

    def __enter__(self):
        # If you want to verify your connection entries were correct uncomment the below, otherwise it is not needed
        #print(f'You entered: {self.host}, {self.user}, {self.password}, {self.database}, {self.port}\n')
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.close()
        print(f'\nConnection has been closed...\n')
        if exc_type:
            print(f'exc_type: {exc_type}')
            print(f'exc_value: {exc_value}')
            print(f'traceback: {traceback}')
        return True

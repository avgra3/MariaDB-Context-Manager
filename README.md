# MariaDB Conext Manager

## Setting Up

Once you have your enviornment set up, run the following in your terminal or command line.

```
pip install -r requirements.txt
```

__Note:__ For Linux or Mac systems, you may need to change "pip" to "pip3".

## Implementing the Context Manager

Before you run your query, make sure that you have MariaDB installed locally or have a connection to a MariaDB database.

If you encounter an error/exception while trying to connect to the database, the connection will be closed and the exception will be printed to the console.

### Example:

```python:
from contextManager import MariaDBCM

# Our query we are using
query = """SELECT * FROM table;"""

# Database connection requirements
host = "HOST"
user = "USER"
password = "PASSWORD"
database = "DATABASE_NAME"
port = PORT

# items to enter: host: str, user: str, password: str, database: str, port: int
with MariaDBCM(host, user, password, password, port) as conn:
    conn.cur.execute(query)
    rows = conn.cur.fetchall()
    
    # Getting data
    for row in rows:
        print(rows[row])
```
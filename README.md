# MariaDB Conext Manager

## Setting Up

Once you have your enviornment set up, run the following in your terminal or command line.

```
pip install -r requirements.txt
```

__Note:__ For Linux or Mac systems, you may need to change "pip" to "pip3".
__Note:__ For Anaconda/Miniconda users, this module is not currently in any repositories, however, you can still use pip to install MariaDB package using the same command as above - but be aware that it may cause conflicts with packages you are using.

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
with MariaDBCM(host, user, password, database, port) as conn:
    conn.cur.execute(query)
    rows = conn.cur.fetchall()
    
    # Getting data
    for row in rows:
        print(rows[row])
```

## Supported Data Types

Several standard python types are converted into SQL types and returned as Python objects when a statement is executed.

| Python Type | SQL Type |
|:--- | :--- |
| None | NULL |
| Bool | TINYINT |
| Float, Double | DOUBLE |
| Decimal | DECIMAL |
| Long | TINYINT, SMALLINT, INT, BIGINT |
| String | VARCHAR, VARSTRING, TEXT |
| ByteArray, Bytes | TINYBLOB, MEDIUMBLOB, BLOB, LONGBLOB |
| DateTime | DATETIME |
| Date | DATE |
| Time | TIME |
| Timestamp | TIMESTAMP |

For more information, see the [documentation](https://mariadb-corporation.github.io/mariadb-connector-python/usage.html) for more information.

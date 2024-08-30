# MariaDB Conext Manager

## Installation

```bash
pip install mariadb-context-manager
```

## Manual Installation

### Setting Up

Once you have your enviornment is set up, run the following in your terminal or command line to get the latest version:

```bash
pip install --upgrade git+https://github.com/avgra3/MariaDB-Context-Manager.git
```

An alternative to this would be to do the following:

```bash
git clone https://github.com/avgra3/MariaDB-Context-Manager.git
cd ./MariaDB-Context-Manager
python -m pip install --upgrade build
python -m build
python -m pip install install ./dist/MariaDB_Context_Manager-0.1.4-py3-none-any.whl
```

__Note:__ For Linux or Mac systems, you may need to change "pip" to "pip3".
__Note:__ For Anaconda/Miniconda users, this module is not currently in any repositories, however, you can still use pip to install MariaDB package using the same command as above - but be aware that it may cause conflicts with packages you are using.

### Implementing the Context Manager

Before you run your query, make sure that you have MariaDB installed locally or have a connection to a MariaDB database.

If you encounter an error/exception while trying to connect to the database, the connection will be closed and the exception will be printed to the console.

#### Example

```python
from contextManager.contextManager import MariaDBCM
import pandas as pd
import polars as pl

# Our query we are using
query = """SELECT * FROM table;"""

# Database connection requirements
host = "HOST"
user = "USER"
password = "PASSWORD"
database = "DATABASE_NAME"
port = 3306 # The default MariaDB port
connection_params = {
    "user": user,
    "password": password,
    "host": host,
    "port": port,
    "database": database,
}

# A dictionary containing results, column names and warnings
with MariaDBCM(**connection_params) as maria:
    result_dictionary = maria.execute(query)

# Show data in a dataframe
# Pandas
df = pd.DataFrame(results["data"], columns=results["columns"])
# Maps the MariaDB data types to Python data types
df = df.astype(results["data_types"])

# Polars
prep = {}
column = 0
for field in result_dictionary["columns"]:
    column_data = [x[column] for x in result_dictionary["data"]]
    prep[field] = column_data
    column+=1

df_pl = pl.DataFrame(prep)
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

from contextManager.contextManager import MariaDBCM
from datetime import datetime


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

# Make our connection object
ourConn = MariaDBCM(**connectionParams)

# Execute a SELECT query
sqlExecute = "SELECT names, balance, dateAdded, timeStamped, dateTime FROM `testDB`.`testTable`;"
sqlExecuteResult = ourConn.execute(query=sqlExecute)
# We expect to get back a dictionary
assert isinstance(sqlExecuteResult, dict)
assert len(sqlExecuteResult["columns"]) == len([
    "names", "balance", "dateAdded", "timeStamped", "dateTime"]) and sorted(sqlExecuteResult["columns"]) == sorted([
        "names", "balance", "dateAdded", "timeStamped", "dateTime"])
assert sqlExecuteResult["statement_ran"] == sqlExecute
assert sqlExecuteResult["rowcount"] == len(sqlExecuteResult["data"])

# We expect to get back a log warning that no query was available
sqlExecuteNoQuery = ""
sqlExecuteResult = ourConn.execute(query=sqlExecuteNoQuery)
assert sqlExecuteResult == {}

# Let's trucnate all data before making changes
sqlTruncate = "TRUNCATE `testDB`.`testTable`;"
ourConn.execute(query=sqlTruncate)

# execute_change: insert
sqlInsert = "INSERT INTO `testDB`.`testTable` (`names`, `balance`, `dateAdded`, `timeStamped`, `dateTime`) VALUES (?, ?, ?, ?, ?);"

NOW = datetime.now()

dataInsert = [
    ("John", 100.01, NOW.date(), NOW, NOW),
    ("Jill", 101.23, NOW.date(), NOW, NOW),
    ("Jason", 97.35, NOW.date(), NOW, NOW),
    ("Justine", 98.99, NOW.date(), NOW, NOW),
    ("Billy", 134.55, NOW.date(), NOW, NOW),
    ("Betty", 139.87, NOW.date(), NOW, NOW),
    ("April", 192.92, NOW.date(), NOW, NOW),
    ("Aspin", 289.23, NOW.date(), NOW, NOW),
    ("Casper", 139.34, NOW.date(), NOW, NOW),
    ("Ingrid", 234.21, NOW.date(), NOW, NOW),
    ("Lois", 204.17, NOW.date(), NOW, NOW),
    ("Gordon", 745.21, NOW.date(), NOW, NOW),
    ("Breann", 247.75, NOW.date(), NOW, NOW),
    ("Anne", 853.46, NOW.date(), NOW, NOW),
    ("Leah", 642.53, NOW.date(), NOW, NOW)]

sqlInsertResult = ourConn.execute_change(
    statement=sqlInsert, parameters=dataInsert)
assert sqlInsertResult["rows_updated"] == len(dataInsert)

# execute_change: update
sqlUpdate = "UPDATE `testDB`.`testTable` SET `dateAdded` = '2025-01-01' WHERE `names` = ?;"
sqlUpdateResult = ourConn.execute_change(
    statement=sqlUpdate, parameters=[("John",)])
assert sqlUpdateResult["statement"] == sqlUpdate
assert sqlUpdateResult["rows_updated"] == 1

# Execute change, with no parameters
sqlUpdate = "UPDATE `testDB`.`testTable` SET `dateAdded` = '2025-01-01' WHERE `names` = 'John';"
sqlUpdateResultNoParams = ourConn.execute_change(statement=sqlUpdate)
assert sqlUpdateResultNoParams == {}

# Execute change, with no statement
sqlUpdateResultNoStatement = ourConn.execute_change(parameters=("John",))
assert sqlUpdateResultNoStatement == {}

# execute_many

# execute_stored_procedure

# verify the results match expected

from src.mariadb_context_manager.contextManager import MariaDBCM
from .constants import connectionParams
from .queries import SIMPLE_SELECT, SIMPLE_TRUNCATE, SIMPLE_INSERTION, SIMPLE_INSERTION_DATA, SIMPLE_UPDATE, EXECUTE_MANY, CREATE_STORED_PROCEDURE

# Make our connection object
ourConn = MariaDBCM(**connectionParams)

# Execute a SELECT query
sqlExecute = SIMPLE_SELECT
sqlExecuteResult = ourConn.run_sql(sql_queries=sqlExecute)
# We expect to get back a dictionary
assert isinstance(sqlExecuteResult, dict)
assert len(sqlExecuteResult["columns"]) == len([
    "names", "balance", "dateAdded", "timeStamped", "dateTime"]) and sorted(sqlExecuteResult["columns"]) == sorted([
        "names", "balance", "dateAdded", "timeStamped", "dateTime"])
assert sqlExecuteResult["statement_ran"] == sqlExecute
assert sqlExecuteResult["rowcount"] == len(sqlExecuteResult["data"])

# We expect to get back a log warning that no query was available
sqlExecuteNoQuery = ""
sqlExecuteResult = ourConn.run_sql(sql_queries=sqlExecuteNoQuery)
assert sqlExecuteResult == {}

# Let's trucnate all data before making changes
sqlTruncate = SIMPLE_TRUNCATE
ourConn.run_sql(sql_queries=sqlTruncate)

# execute_change: insert
sqlInsert = SIMPLE_INSERTION
dataInsert = SIMPLE_INSERTION_DATA

sqlInsertResult = ourConn.run_sql(
    sqlInsert, data=dataInsert)
assert sqlInsertResult["rows_updated"] == len(dataInsert)

# execute_change: update
sqlUpdate = SIMPLE_UPDATE
sqlUpdateResult = ourConn.run_sql(sqlUpdate, data=[("John",)])
assert sqlUpdateResult["statement"] == sqlUpdate
assert sqlUpdateResult[0].metadata["updated"] == 1

# Execute change, with no parameters
sqlUpdate = "UPDATE `testDB`.`testTable` SET `dateAdded` = '2025-01-01' WHERE `names` = 'John';"
sqlUpdateResultNoParams = ourConn.run_sql(sqlUpdate)
assert sqlUpdateResultNoParams == {}

# Execute change, with no statement
sqlUpdateResultNoStatement = ourConn.run_sql("", data=("John",))
assert sqlUpdateResultNoStatement == {}

# execute_many
sqlExecuteMany = EXECUTE_MANY
sqlExecuteManyResult = ourConn.run_sql(sqlExecuteMany)
assert len(sqlExecuteManyResult) == 2

# execute_stored_procedure
# Need to first create the procedure
sqlCreateStoredProcedure = CREATE_STORED_PROCEDURE
sqlCreateStoredProcedure = createdStoredProcedure = ourConn.run_sql(sqlCreateStoredProcedure)

# We expect nothing retured for creating a stored procedure
assert len(createdStoredProcedure) == 0
assert isinstance(createdStoredProcedure, dict)

# Now check we can use the created stored procedure
# storedProcedureName = "getJohn"
# sqlExecuteStoredProcedure = ourConn.execute_stored_procedure(
#     stored_procedure_name=storedProcedureName,
#     inputs=("",),
# )
# assert sqlExecuteStoredProcedure["data"][0] == ("John",)
# assert sqlExecuteStoredProcedure["columns"][0] == "johns_name"
# assert sqlExecuteStoredProcedure["rowcount"] == 1
# assert sqlExecuteStoredProcedure["warnings"] == 0
# assert sqlExecuteStoredProcedure["data_types"]["johns_name"] == "str"

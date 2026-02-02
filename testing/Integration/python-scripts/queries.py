from datetime import datetime

SIMPLE_SELECT: str = "SELECT names, balance, dateAdded, timeStamped, dateTime FROM `testDB`.`testTable`;"

SIMPLE_TRUNCATE: str = "TRUNCATE `testDB`.`testTable`;"

SIMPLE_INSERTION: str = "INSERT INTO `testDB`.`testTable` (`names`, `balance`, `dateAdded`, `timeStamped`, `dateTime`) VALUES (?, ?, ?, ?, ?);"

NOW = datetime.now()

SIMPLE_INSERTION_DATA = [
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

SIMPLE_UPDATE: str = "UPDATE `testDB`.`testTable` SET `dateAdded` = '2025-01-01' WHERE `names` = ?;"

EXECUTE_MANY: str = "SELECT `names` FROM `testDB`.`testTable` WHERE `names`='John'; SELECT `names` FROM `testDB`.`testTable` WHERE `names`='John';"

CREATE_STORED_PROCEDURE: str = """
    CREATE OR REPLACE PROCEDURE getJohn(OUT johns_name VARCHAR(50))
    BEGIN
        SELECT `names` INTO johns_name FROM `testDB`.`testTable` WHERE `names`='John';
    END
"""


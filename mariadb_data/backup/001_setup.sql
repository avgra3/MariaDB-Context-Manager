-- create database if not exists
CREATE OR REPLACE DATABASE `testDB`;

-- Set default engine
ALTER DATABASE `testDB` CHARACTER SET `utf8mb4` COLLATE `utf8mb4_unicode_520_ci`;

-- create the user if not exists
CREATE OR REPLACE USER "testUser"@"%" IDENTIFIED BY "testUserPassword";

-- Grant user privleges
GRANT ALL PRIVILEGES ON *.* TO 'testUser'@'%' IDENTIFIED BY "testUserPassword";

-- create sample table
CREATE TABLE IF NOT EXISTS `testDB`.`testTable` (
	`id` INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
	`names` VARCHAR(40) DEFAULT NULL,
	`balance` DECIMAL(14, 1) DEFAULT NULL,
	`dateAdded` DATE DEFAULT NULL,
	`timeStamped` TIMESTAMP DEFAULT NULL,
	`dateTime` DATETIME DEFAULT NULL,
	PRIMARY KEY (`id`)
) ENGINE = MYISAM DEFAULT CHARSET= utf8mb4 COLLATE= utf8mb4_unicode_520_ci PAGE_CHECKSUM=0, ROW_FORMAT=DYNAMIC;

-- insert data
REPLACE INTO `testDB`.`testTable`
(`names`, `balance`, `dateAdded`, `timeStamped`, `dateTime`)
VALUES
("John", 100.01, NOW(), NOW(),  NOW()),
("Jill", 101.23, NOW(), NOW(), NOW()),
("Jason", 97.35, NOW(), NOW(), NOW()),
("Justine", 98.99, NOW(), NOW(), NOW()),
("Billy", 134.55, NOW(), NOW(), NOW()),
("Betty", 139.87, NOW(), NOW(), NOW()),
("April", 192.92, NOW(), NOW(), NOW()),
("Aspin", 289.23, NOW(), NOW(), NOW()),
("Casper", 139.34, NOW(), NOW(), NOW()),
("Ingrid", 234.21, NOW(), NOW(), NOW()),
("Lois", 204.17, NOW(), NOW(), NOW()),
("Gordon", 745.21, NOW(), NOW(), NOW()),
("Breann", 247.75, NOW(), NOW(), NOW()),
("Anne", 853.46, NOW(), NOW(), NOW()),
("Leah", 642.53, NOW(), NOW(), NOW());

-- Quick optimize
OPTIMIZE TABLE `testDB`.`testTable`;

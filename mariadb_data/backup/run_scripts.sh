#!/bin/bash
echo "Creating database, tables, and users"
mariadb --host="localhost" --port=3306 --user=root -p$MARIADB_ROOT_PASSWORD < /backup/001_setup.sql

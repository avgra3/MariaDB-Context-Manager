#!/bin/sh

docker build -t mariadbcm:latest .
docker compose -f docker-compose.yml up --force-recreate -d
docker compose logs -f

#!/bin/bash

# Create docker network
# docker network create --subnet=172.20.0.0/16 testing_MCM

# Prune networks
docker network prune --force
docker system prune --all --force

# Set env variable
# export COMPOSE_BAKE=true

# Main script to build and test our database
docker compose up --force-recreate \
	-y


#!/bin/bash

# Set env variable
# export COMPOSE_BAKE=true

# Main script to build and test our database
docker compose up --force-recreate \
	--abort-on-container-exit \
	-y

test:
	uv run python -m unittest discover -s tests -vvv
check:
	uv run ruff check ./src
integration:
	docker compose up --force-recreate --abort-on-container-exit -y
	


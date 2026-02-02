FROM debian:stable-slim

# Get the current main directory
COPY . .

# Adds uv
ENV PYTHON_VERSION=3.11
COPY --from=ghcr.io/astral-sh/uv:latest /uv/ /uvx/ /bin/

# Normal updates to image & addition of mariadb-connector-c
RUN apt update && \
	apt upgrade -y && \
	apt install -y curl ca-certificates gcc && \
	apt install -y libmariadb3 libmariadb-dev && \
	# Run our integration testing && \
	uv python install $PYTHON_VERSION && \
	uv venv --python $PYTHON_VERSION && \
	uv sync

ENTRYPOINT ["uv", "run", "python", "-m", "unittest", "discover", "-s" "tests", "-vvv"]

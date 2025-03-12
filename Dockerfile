FROM debian:stable-slim

# Adds uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv/ /uvx/ /bin/

# Normal updates to image & addition of mariadb-connector-c
RUN apt-get update && \
	apt-get install -y curl ca-certificates gcc && \
	apt-get install -y libmariadb3 libmariadb-dev

# Get srcFiles
COPY ./pyproject.toml /srcFiles/
COPY ./setup.cfg /srcFiles/
COPY ./setup.py /srcFiles/
COPY ./testing /srcFiles/
COPY ./src/ /srcFiles/src/
COPY ./README.md /srcFiles/

# Install minimum Python version (3.9)
RUN uv python install 3.9

# Install from srcFiles
WORKDIR /srcFiles

# Create a virtual ".env", with minimum Python version
RUN uv venv --python 3.9

# Add the python mariadb connector
RUN uv pip install mariadb

# Build our package
RUN uv build


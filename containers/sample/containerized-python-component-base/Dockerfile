FROM python:3.10-buster

RUN pip install poetry==1.6.1

ENV POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN --mount=type=cache,target=$POETRY_CACHE_DIR poetry install --no-root --no-interaction

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

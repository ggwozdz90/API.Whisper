# Description: Dockerfile for building the API Whisper image
FROM python:3.11.9-slim-bookworm as builder

RUN pip install poetry==1.8.3

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app
COPY pyproject.toml poetry.lock ./
COPY apiwhisper ./apiwhisper
COPY runserver.py runserver.py

RUN poetry install --without dev --no-root && rm -rf $POETRY_CACHE_DIR

# Runtime image
FROM python:3.11.9-slim-bookworm as runtime

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

RUN apt-get update && apt-get install -y ffmpeg

WORKDIR /app
COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}
COPY apiwhisper ./apiwhisper
COPY runserver.py runserver.py

EXPOSE 8000

ENTRYPOINT ["python", "-m", "runserver"]
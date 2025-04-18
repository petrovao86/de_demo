# Установка poetry
FROM python:3.12.9-slim-bookworm AS builder

WORKDIR /app/

RUN apt update && \
    apt install --no-install-recommends -y curl && \
    curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false && \
    apt remove -y curl && \
    apt autoremove -y && \
    apt purge -y $(dpkg -l | grep '^rc' | awk '{print $2}') && \
    rm -rf /var/lib/apt/lists

# Кеширование зависимостей проекта
FROM builder AS cache
COPY ./poetry.lock* ./pyproject.toml /app/
RUN poetry self add poetry-plugin-export && \
    poetry export --all-extras --without-hashes --output=requirements.txt && \
    pip download  -r requirements.txt -d /app/dist

# Сборка пакета
FROM builder AS build

COPY --from=cache /app /app
COPY ./de_demo /app/de_demo
RUN poetry build

# Базовый слой пакета
FROM python:3.12.9-slim-bookworm AS base

RUN adduser --system --home /app --uid 1000 --group app
USER app

WORKDIR /app/
ENV PATH="/app/.local/bin:${PATH}"

# Консольное приложение без служб
FROM base AS app

RUN --mount=type=bind,from=build,source=/app/dist,target=/app/dist pip install \
    --user  \
    --no-cache-dir  \
    --no-index  \
    --find-links /app/dist  \
    de_demo
ENTRYPOINT  ["de-demo"]

# Только API
FROM base AS api

RUN --mount=type=bind,from=build,source=/app/dist,target=/app/dist pip install \
    --user \
    --no-cache-dir \
    --no-index \
    --find-links /app/dist \
    de_demo[api]
ENTRYPOINT  ["de-demo", "run", "api"]

# Dagster с dbt
FROM base AS dagster

RUN --mount=type=bind,from=build,source=/app/dist,target=/app/dist pip install \
    --user \
    --no-cache-dir \
    --no-index \
    --find-links /app/dist  \
    de_demo[dagster,dbt]

COPY --chown=app:app dbt /app/dbt
RUN dbt parse \
    --target dev \
    --profiles-dir /app/dbt \
    --project-dir /app/dbt \
    --log-level-file none \
    --no-send-anonymous-usage-stats

COPY --chown=app:app dagster.yaml /app/

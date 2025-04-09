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
    poetry export --without-hashes --output=requirements.txt && \
    pip download  -r requirements.txt -d /app/dist

# Сборка пакета
FROM builder AS build

COPY --from=cache /app /app
COPY ./de_demo /app/de_demo
RUN poetry build

FROM builder AS dbt_build

ENV PATH="/root/.local/bin:${PATH}"

COPY --from=cache /app /app
COPY dbt /app/dbt
RUN poetry self add poetry-plugin-export && \
    poetry export --without-hashes --extras=dbt --output=requirements.txt && \
    pip install --user --no-cache-dir --no-index --find-links /app/dist -r requirements.txt && \
    cd /app/dbt && \
    dbt parse --target parse --profiles-dir /app/dbt
# Установка пакета
FROM python:3.12.9-slim-bookworm AS app

RUN adduser --system --home /app --uid 1000 --group app
USER app

WORKDIR /app/
ENV PATH="/app/.local/bin:${PATH}"

COPY dagster.yaml /app/
COPY dbt /app/dbt
COPY --from=build --chown=app:app /app/dist /app/dist
COPY --from=dbt_build --chown=app:app /app/dbt/target/manifest.json /app/dbt/target/manifest.json
RUN pip install --user --no-cache-dir --no-index --find-links /app/dist de_demo[dbt]

ENTRYPOINT  ["de-demo"]
FROM python:3.9.14-slim-bullseye as base

ENV LANG=C.UTF-8 \
    DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

RUN apt-get update && apt-get install -y --no-install-recommends -qq gcc=4:10.2.1-1 g++=4:10.2.1-1 curl=7.74.0-1.3+deb11u3 \
 && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

FROM base as builder

ENV POETRY_VERSION=1.1.13 \
    POETRY_HOME="/opt/poetry"

SHELL ["/bin/bash", "-o", "pipefail", "-c"]
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="$POETRY_HOME/bin:$PATH"

COPY pyproject.toml poetry.lock ./
RUN python -m venv --copies /venv

RUN . /venv/bin/activate && poetry install --no-dev --no-root

FROM base as production

COPY --from=builder /venv /venv

RUN mkdir -p /var/www && chown www-data /var/www && \
    chown -R www-data /app/ && chown -R www-data /venv

ENV PYTHONPATH="/venv/lib/python3.9/site-packages/"
ENV PATH=$PATH:/venv/bin
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PULSE_SERVER_PORT 8000
ENV PROMETHEUS_PORT 8000

EXPOSE $PROMETHEUS_PORT
USER www-data

COPY --from=builder /usr/local/ /usr/local/
COPY assets ./assets
COPY src ./

HEALTHCHECK --interval=10s --timeout=3s \
    CMD curl -f http://localhost:$PULSE_SERVER_PORT/healthcheck || exit 1

ENTRYPOINT ["python3", "-u", "src/oracle.py"]

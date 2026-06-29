FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1

WORKDIR /app

RUN python -m pip install --upgrade pip

RUN pip install poetry

COPY pyproject.toml poetry.lock README.md ./
COPY . .
RUN chmod +x boot.sh

RUN poetry install --only main

RUN mkdir -p /app/data

EXPOSE 8000
ENTRYPOINT ["./boot.sh"]

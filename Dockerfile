FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock README.md ./

RUN poetry install

COPY . .
RUN chmod +x boot.sh

RUN mkdir -p /app/data

EXPOSE 8000
ENTRYPOINT ["./boot.sh"]

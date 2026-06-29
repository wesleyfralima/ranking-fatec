#!/usr/bin/env bash

set -e

echo "========================================"
echo "Aplicando migrations..."
echo "========================================"

alembic upgrade head

echo "========================================"
echo "Inserindo dados iniciais..."
echo "========================================"

poetry run popular-banco

echo "========================================"
echo "Iniciando aplicação..."
echo "========================================"

exec uvicorn ranking_fatec.main:app \
    --host 127.0.0.1 \
    --port 8000

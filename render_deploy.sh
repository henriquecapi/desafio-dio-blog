#!/usr/bin/env bash
# Sair imediatamente se um comando falhar
set -e

# Define o PYTHONPATH para que as migrações encontrem o módulo 'config'
export PYTHONPATH=src

echo "Running migrations..."
poetry run alembic upgrade head

echo "Starting server..."
poetry run uvicorn main:app --host 0.0.0.0 --port $PORT
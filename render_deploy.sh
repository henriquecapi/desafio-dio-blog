#!/usr/bin/env bash
# Sair imediatamente se um comando falhar
set -e

echo "Running migrations..."
poetry run alembic upgrade head

echo "Starting server..."
poetry run uvicorn src.main:app --host 0.0.0.0 --port $PORT
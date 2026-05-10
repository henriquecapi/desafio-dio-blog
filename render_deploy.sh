#!/usr/bin/env bash
# Sair imediatamente se um comando falhar
set -e

# Define o PYTHONPATH para que as migrações encontrem o módulo 'config'
export PYTHONPATH=src

echo "--- Diagnostic Step ---"
echo "Checking if DATABASE_URL is set..."
if [ -z "$DATABASE_URL" ]; then
    echo "ERROR: DATABASE_URL environment variable is NOT set in Render!"
    exit 1
fi

echo "Verifying application configuration..."
poetry run python -c "from config import settings; print('Configuração carregada com sucesso!')" || { echo 'Falha ao carregar configurações. Verifique os caminhos e variáveis de ambiente.'; exit 1; }

echo "--- Starting Migrations ---"
poetry run alembic upgrade head

echo "--- Starting Server ---"
poetry run uvicorn main:app --host 0.0.0.0 --port $PORT
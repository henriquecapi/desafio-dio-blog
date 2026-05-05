import asyncio
import os
import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from unittest.mock import patch
import sqlalchemy as sa
import databases

# Configuração global para garantir que o sistema de teste use um banco separado
# sem alterar o código original em src/
TEST_DATABASE_URL = "sqlite:///tests.db"
test_engine = sa.create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
test_db = databases.Database(TEST_DATABASE_URL)

# Iniciamos o patch antes de qualquer outra coisa ser importada
patcher_url = patch("database.DATABASE_URL", TEST_DATABASE_URL)
patcher_engine = patch("database.engine", test_engine)
patcher_db = patch("database.database", test_db)

patcher_url.start()
patcher_engine.start()
patcher_db.start()

@pytest.fixture(scope="session", autouse=True)
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest_asyncio.fixture(autouse=True)
async def db():
    from database import metadata
    
    # Cria as tabelas no banco de teste
    metadata.create_all(test_engine)
    await test_db.connect()
    
    yield test_db
    
    await test_db.disconnect()
    metadata.drop_all(test_engine)
    
    # Remove o arquivo de teste se existir
    if os.path.exists("tests.db"):
        try:
            os.remove("tests.db")
        except PermissionError:
            pass

@pytest_asyncio.fixture
async def client():
    from main import app
    
    transport = ASGITransport(app=app)
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    async with AsyncClient(
        base_url="http://test", transport=transport, headers=headers
    ) as client:
        yield client

@pytest_asyncio.fixture
async def access_token(client: AsyncClient):
    # O login não valida banco de dados no sistema atual, apenas gera o JWT
    response = await client.post("/auth/login", json={"user_id": 1})
    return response.json()["access_token"]

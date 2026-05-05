import pytest
import pytest_asyncio
from fastapi import status
from httpx import AsyncClient

@pytest_asyncio.fixture(autouse=True)
async def populate_posts(db):
    """
    Popula o banco de dados antes de cada teste de leitura.
    Note que o PostIn original só aceita 'title' e 'content'.
    O sistema define 'published' como False por padrão.
    """
    from schemas.post import PostIn
    from services.post import PostService

    service = PostService()
    # Criamos 4 posts para testar a paginação (o limite padrão do sistema é 3)
    await service.create_post(PostIn(title="Post 1", content="Conteúdo 1"))
    await service.create_post(PostIn(title="Post 2", content="Conteúdo 2"))
    await service.create_post(PostIn(title="Post 3", content="Conteúdo 3"))
    await service.create_post(PostIn(title="Post 4", content="Conteúdo 4"))

async def test_read_posts_first_page_success(client: AsyncClient, access_token: str):
    """Testa a listagem da primeira página (deve retornar 3 posts devido ao limite fixo)."""
    # Given
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"pag": 1}

    # When
    response = await client.get("/posts/", params=params, headers=headers)

    # Then
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 3
    assert content[0]["title"] == "Post 1"

async def test_read_posts_second_page_success(client: AsyncClient, access_token: str):
    """Testa a listagem da segunda página (deve retornar o 4º post)."""
    # Given
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"pag": 2}

    # When
    response = await client.get("/posts/", params=params, headers=headers)

    # Then
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 1
    assert content[0]["title"] == "Post 4"

async def test_read_posts_no_auth_fail(client: AsyncClient):
    """Valida que o acesso sem token retorna 401."""
    # When
    response = await client.get("/posts/")

    # Then
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

async def test_read_posts_default_page_success(client: AsyncClient, access_token: str):
    """Valida que o sistema usa pag=1 por padrão se não informado."""
    # Given
    headers = {"Authorization": f"Bearer {access_token}"}

    # When
    response = await client.get("/posts/", headers=headers)

    # Then
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 3

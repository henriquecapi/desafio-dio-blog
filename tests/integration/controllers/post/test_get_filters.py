import pytest
import pytest_asyncio
from fastapi import status
from httpx import AsyncClient

@pytest_asyncio.fixture(autouse=True)
async def populate_posts(db):
    from schemas.post import PostIn
    from services.post import PostService

    service = PostService()
    await service.create_post(PostIn(title="Python FastAPI", content="Aprendendo a criar APIs"))
    await service.create_post(PostIn(title="Javascript Node", content="Desenvolvimento web moderno"))
    await service.create_post(PostIn(title="Python Avançado", content="Deep dive no ecossistema Python"))

async def test_get_posts_by_title_success(client: AsyncClient, access_token: str):
    """Testa a busca de posts por termo no título."""
    # Given
    headers = {"Authorization": f"Bearer {access_token}"}
    title_query = "Python"

    # When
    response = await client.get(f"/posts/title/{title_query}", headers=headers)

    # Then
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 2
    assert "Python" in content[0]["title"]
    assert "Python" in content[1]["title"]

async def test_get_posts_by_content_success(client: AsyncClient, access_token: str):
    """Testa a busca de posts por termo no conteúdo."""
    # Given
    headers = {"Authorization": f"Bearer {access_token}"}
    content_query = "moderno"

    # When
    response = await client.get(f"/posts/content/{content_query}", headers=headers)

    # Then
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 1
    assert "moderno" in content[0]["content"]

async def test_get_posts_by_id_query_success(client: AsyncClient, access_token: str):
    """Testa a filtragem de posts por ID via query parameter (?id=1)."""
    # Given
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"id": 1}

    # When
    response = await client.get("/posts/", params=params, headers=headers)

    # Then
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert len(content) == 1
    assert content[0]["id"] == 1
    assert content[0]["title"] == "Python FastAPI"

async def test_get_posts_by_title_empty_result_success(client: AsyncClient, access_token: str):
    """Valida que retorna lista vazia se nenhum título bater."""
    # Given
    headers = {"Authorization": f"Bearer {access_token}"}
    title_query = "Inexistente"

    # When
    response = await client.get(f"/posts/title/{title_query}", headers=headers)

    # Then
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 0

import pytest
import pytest_asyncio
from fastapi import status
from httpx import AsyncClient

@pytest_asyncio.fixture(autouse=True)
async def populate_posts(db):
    from schemas.post import PostIn
    from services.post import PostService

    service = PostService()
    await service.create_post(PostIn(title="Target Post", content="Target Content"))

async def test_get_post_by_id_success(client: AsyncClient, access_token: str):
    """Testa a busca de um post existente por ID."""
    # Given
    headers = {"Authorization": f"Bearer {access_token}"}
    post_id = 1

    # When
    response = await client.get(f"/posts/{post_id}", headers=headers)

    # Then
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == post_id
    assert response.json()["title"] == "Target Post"

async def test_get_post_by_id_not_found_fail(client: AsyncClient, access_token: str):
    """Valida que retornar 404 para ID inexistente."""
    # Given
    headers = {"Authorization": f"Bearer {access_token}"}
    post_id = 999

    # When
    response = await client.get(f"/posts/{post_id}", headers=headers)

    # Then
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Post não encontrado."

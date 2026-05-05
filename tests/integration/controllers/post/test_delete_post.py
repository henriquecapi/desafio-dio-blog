import pytest_asyncio
from fastapi import status
from httpx import AsyncClient

@pytest_asyncio.fixture(autouse=True)
async def populate_posts(db):
    from schemas.post import PostIn
    from services.post import PostService
    service = PostService()
    await service.create_post(PostIn(title="Post para Deletar", content="Conteúdo"))

async def test_delete_post_success(client: AsyncClient, access_token: str):
    """Testa a remoção de um post existente."""
    # Given
    headers = {"Authorization": f"Bearer {access_token}"}
    post_id = 1

    # When
    response = await client.delete(f"/posts/{post_id}", headers=headers)

    # Then
    assert response.status_code == status.HTTP_204_NO_CONTENT

async def test_delete_post_not_found_fail(client: AsyncClient, access_token: str):
    """Testa erro 404 ao tentar deletar post que não existe."""
    # Given
    headers = {"Authorization": f"Bearer {access_token}"}
    post_id = 999

    # When
    response = await client.delete(f"/posts/{post_id}", headers=headers)

    # Then
    assert response.status_code == status.HTTP_404_NOT_FOUND

async def test_publish_post_success(client: AsyncClient, access_token: str):
    """
    Testa a rota de publicação (PATCH /posts/published/{id}).
    Esta rota existe no sistema original.
    """
    # Given
    headers = {"Authorization": f"Bearer {access_token}"}
    post_id = 1

    # When
    response = await client.patch(f"/posts/published/{post_id}", headers=headers)

    # Then
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["published"] is True

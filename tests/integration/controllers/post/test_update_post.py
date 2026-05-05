import pytest_asyncio
from fastapi import status
from httpx import AsyncClient

@pytest_asyncio.fixture(autouse=True)
async def populate_posts(db):
    from schemas.post import PostIn
    from services.post import PostService
    service = PostService()
    await service.create_post(PostIn(title="Post Original", content="Conteúdo Original"))

async def test_update_post_title_success(client: AsyncClient, access_token: str):
    """Testa a atualização do título de um post."""
    # Given
    headers = {"Authorization": f"Bearer {access_token}"}
    data = {"title": "Título Atualizado"}
    post_id = 1

    # When
    response = await client.patch(f"/posts/{post_id}", json=data, headers=headers)

    # Then
    assert response.status_code == status.HTTP_200_OK
    content = response.json()
    assert content["title"] == "Título Atualizado"
    assert content["content"] == "Conteúdo Original"

async def test_update_post_empty_payload_fail(client: AsyncClient, access_token: str):
    """Testa falha ao enviar payload vazio (validado no serviço)."""
    # Given
    headers = {"Authorization": f"Bearer {access_token}"}
    data = {}
    post_id = 1

    # When
    response = await client.patch(f"/posts/{post_id}", json=data, headers=headers)

    # Then
    # O serviço retorna 400 se nenhum campo informado
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Nenhum campo informado para atualização."

async def test_update_post_not_found_fail(client: AsyncClient, access_token: str):
    """Testa erro 404 ao atualizar post inexistente."""
    # Given
    headers = {"Authorization": f"Bearer {access_token}"}
    data = {"title": "Novo Título"}
    post_id = 999

    # When
    response = await client.patch(f"/posts/{post_id}", json=data, headers=headers)

    # Then
    assert response.status_code == status.HTTP_404_NOT_FOUND
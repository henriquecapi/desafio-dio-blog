from fastapi import status
from httpx import AsyncClient

async def test_create_post_success(client: AsyncClient, access_token: str):
    """Testa a criação de um post com sucesso."""
    # Given
    headers = {"Authorization": f"Bearer {access_token}"}
    data = {
        "title": "Novo Post de Teste",
        "content": "Conteúdo interessante aqui"
    }

    # When
    response = await client.post("/posts/", json=data, headers=headers)

    # Then
    assert response.status_code == status.HTTP_201_CREATED
    content = response.json()
    assert content["title"] == data["title"]
    assert content["id"] is not None
    assert content["published"] is False  # O sistema define False por padrão

async def test_create_post_missing_title_fail(client: AsyncClient, access_token: str):
    """Testa falha na criação sem título (validado manualmente no serviço)."""
    # Given
    headers = {"Authorization": f"Bearer {access_token}"}
    data = {
        "content": "Conteúdo sem título"
    }

    # When
    response = await client.post("/posts/", json=data, headers=headers)

    # Then
    # O sistema original retorna 400 se o título for None ou vazio
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "O título é obrigatório."

async def test_create_post_missing_content_fail(client: AsyncClient, access_token: str):
    """Testa falha na criação sem conteúdo (validado manualmente no serviço)."""
    # Given
    headers = {"Authorization": f"Bearer {access_token}"}
    data = {
        "title": "Título sem conteúdo"
    }

    # When
    response = await client.post("/posts/", json=data, headers=headers)

    # Then
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "O conteúdo é obrigatório."

async def test_create_post_invalid_token_fail(client: AsyncClient):
    """Testa falha com token inválido."""
    # Given
    headers = {"Authorization": "Bearer token-invalido"}
    data = {"title": "T", "content": "C"}

    # When
    response = await client.post("/posts/", json=data, headers=headers)

    # Then
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

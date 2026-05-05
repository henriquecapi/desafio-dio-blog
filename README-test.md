# Guia de Testes - Capi Blog

Este documento descreve detalhadamente a suíte de testes de integração do projeto **Capi Blog**. Os testes foram projetados para validar o comportamento do sistema sem alterar o código original ou o banco de dados de produção.

---

## 1. Configuração e Isolamento (conftest.py)

Para garantir que seu banco de dados `blog.sqlite` nunca seja afetado pelos testes, utilizamos uma estratégia de isolamento:

- **Redirecionamento do Banco**: O arquivo `conftest.py` intercepta a conexão do sistema e a redireciona para um arquivo temporário chamado `tests.db`.
- **Fixtures**:
    - `db`: Prepara o banco de teste, cria as tabelas e limpa tudo após cada teste.
    - `client`: Um cliente HTTP assíncrono que simula requisições à API.
    - `access_token`: Gera um token JWT válido para testar rotas protegidas.

---

## 2. Testes de Autenticação (auth/test_login.py)

### `test_login_success`
- **O que faz**: Envia um ID de usuário para a rota `/auth/login`.
- **Esperado**: Receber um status `200 OK` e um `access_token` no formato string.
- **Nota**: Atualmente, o sistema apenas gera o token sem validar se o usuário existe no banco.

---

## 3. Testes de Posts (post/)

### A. Criação (`test_create_post.py`)

1. **`test_create_post_success`**:
    - **Ação**: Envia um título e conteúdo válidos com token JWT.
    - **Esperado**: Status `201 Created`. O post deve ter `published=False` por padrão e um ID gerado.
2. **`test_create_post_missing_title_fail`**:
    - **Ação**: Tenta criar um post sem o campo `title`.
    - **Esperado**: Status `400 Bad Request` com a mensagem `"O título é obrigatório."`.
3. **`test_create_post_missing_content_fail`**:
    - **Ação**: Tenta criar um post sem o campo `content`.
    - **Esperado**: Status `400 Bad Request` com a mensagem `"O conteúdo é obrigatório."`.
4. **`test_create_post_invalid_token_fail`**:
    - **Ação**: Tenta criar um post com um token JWT malformado.
    - **Esperado**: Status `401 Unauthorized`.

### B. Listagem e Paginação (`test_read_all.py`)

1. **`test_read_posts_first_page_success`**:
    - **Ação**: Solicita a página 1 (`pag=1`).
    - **Esperado**: Receber 3 posts (o limite é fixo em 3 no sistema).
2. **`test_read_posts_second_page_success`**:
    - **Ação**: Solicita a página 2 (`pag=2`) após criar 4 posts.
    - **Esperado**: Receber apenas 1 post (o que sobrou da primeira página).
3. **`test_read_posts_default_page_success`**:
    - **Ação**: Chama `/posts/` sem passar o parâmetro `pag`.
    - **Esperado**: O sistema deve assumir a página 1 e retornar os primeiros posts.

### C. Atualização (`test_update_post.py`)

1. **`test_update_post_title_success`**:
    - **Ação**: Atualiza apenas o título de um post existente via `PATCH`.
    - **Esperado**: Status `200 OK`. O título deve mudar, mas o conteúdo original deve ser preservado.
2. **`test_update_post_empty_payload_fail`**:
    - **Ação**: Envia um `PATCH` com corpo vazio `{}`.
    - **Esperado**: Status `400 Bad Request` com a mensagem `"Nenhum campo informado para atualização."`.

### D. Remoção e Publicação (`test_delete_post.py`)

1. **`test_delete_post_success`**:
    - **Ação**: Deleta um post pelo seu ID.
    - **Esperado**: Status `204 No Content`.
2. **`test_delete_post_not_found_fail`**:
    - **Ação**: Tenta deletar um ID que não existe (ex: 999).
    - **Esperado**: Status `404 Not Found`.
3. **`test_publish_post_success`**:
    - **Ação**: Chama a rota especial `/posts/published/{id}`.
    - **Esperado**: Status `200 OK` e o campo `published` deve mudar de `False` para `True`.

---

## 4. Resumo de Comportamentos do Sistema

Ao ler os testes, você notará algumas regras fixas do seu sistema atual:
- **Limite de Paginação**: Está travado em **3 posts** por vez.
- **Campos Obrigatórios**: O sistema exige `title` e `content` através de verificações manuais no arquivo `services/post.py`.
- **Estado Inicial**: Todo post nasce como **não publicado** (`published=False`).
- **Rotas Ausentes**: Não existe atualmente uma rota para buscar um post individual por ID (`GET /posts/{id}`), por isso não há testes para essa funcionalidade.

---
*Este arquivo foi gerado para auxiliar no aprendizado da estrutura de testes automatizados.*

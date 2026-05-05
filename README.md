# FastAPI Blog API 🚀

Este é um projeto de uma API de Blog desenvolvida com **FastAPI**, utilizando uma arquitetura moderna e assíncrona. O sistema permite o gerenciamento completo de postagens, desde a criação como rascunho até a publicação e exclusão.

## 🏗️ Arquitetura do Sistema

### Evolução Arquitetural
Inicialmente, o projeto seguia um modelo onde a lógica de negócio e as rotas estavam misturadas no controller. Para garantir a manutenibilidade, migramos para o padrão **Service Layer**:

1.  **Separação de Preocupações**: O Controller agora lida apenas com o protocolo HTTP (status codes, rotas, schemas). A lógica "do que acontece com os dados" foi movida para o Service.
2.  **Reutilização**: Se precisarmos criar uma interface de linha de comando (CLI) ou um worker em background, podemos reutilizar o `PostService` sem tocar nas rotas.
3.  **Tipagem Forte**: Implementamos o uso do `databases.interfaces.Record`, garantindo que os dados que trafegam entre o banco e o service sejam íntegros e bem definidos.

### Componentes:
-   **Controllers (`controllers/`)**: Porteiros da aplicação.
-   **Services (`services/`)**: Onde a "mágica" acontece (lógica de negócio).
-   **Models (`models/`)**: Definição das tabelas com SQLAlchemy Core.
-   **Schemas/Views (`schemas/`, `views/`)**: Contratos de entrada e saída de dados.
-   **Database (`database.py`)**: Gerenciamento da conexão assíncrona.

---

## 📊 Estrutura de Dados (Tabela `posts`)

Abaixo estão os campos que compõem a entidade principal do sistema:

| Campo          | Tipo         | Descrição                                      |
| :------------- | :----------- | :--------------------------------------------- |
| `id`           | Integer      | Chave primária (Auto-incremento).              |
| `title`        | String(150)  | Título único do post.                          |
| `content`      | String       | Conteúdo textual da postagem.                  |
| `published_at` | DateTime     | Data de criação ou última alteração.           |
| `published`    | Boolean      | Status: `True` (Publicado), `False` (Rascunho). |

---

## 📂 Estrutura de Arquivos

```text
capi-blog/
├── src/
│   ├── controllers/      # Rotas e Endpoints (HTTP)
│   │   └── post.py
│   ├── models/           # Definições de Tabelas (SQLAlchemy)
│   │   └── post.py
│   ├── schemas/          # Modelos Pydantic de Entrada (Validations)
│   │   └── post.py
│   ├── services/         # Lógica de Negócio (Services)
│   │   └── post.py
│   ├── views/            # Modelos Pydantic de Saída (View Models)
│   │   └── post.py
│   ├── database.py       # Configuração da conexão com o Banco
│   ├── main.py           # Ponto de entrada da aplicação (FastAPI)
│   └── security.py       # Segurança e JWT
├── pyproject.toml    # Configurações do Poetry e Formatação
├── README.md         # Documentação do Projeto
└── blog.sqlite       # Banco de dados (gerado automaticamente)
```

---

## ✨ Funcionalidades e Melhorias

### 1. CRUD Completo de Posts
-   **Paginação**: `GET /posts/?pag=1` com limite fixo de 3 itens.
-   **Criação**: `POST /posts/` (Gera rascunho automático).
-   **Edição**: `PATCH /posts/{id}` (Atualização parcial e reset de status).
-   **Publicação**: `PATCH /posts/published/{id}`.
-   **Deleção**: `DELETE /posts/{id}`.

### 2. Validações e DX (Developer Experience)
-   **Mensagens em Português**: Erros de validação personalizados.
-   **Swagger Organizado**: Uso de Tags para agrupar as rotas no painel `/docs`.
-   **Formatação Automática**: Integração com **Black** e **isort** para código limpo.

## 🚀 Como Executar

1.  Instale as dependências: `poetry install`
2.  Inicie o servidor: `poetry run uvicorn src.main:app --reload`
3.  Acesse: `http://127.0.0.1:8000/docs`

---
*Documentação atualizada para refletir a nova arquitetura orientada a serviços.*

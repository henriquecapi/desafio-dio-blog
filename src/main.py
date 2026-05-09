from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from controllers import auth, post
from database import database, engine, metadata
from exceptions import (BadRequestError, ConflictError, NotFoundPostError,
                        NotFoundUserError)


# A função lifespan gerencia o ciclo de vida da aplicação.
# (startup -> lifespan -> shutdown)
@asynccontextmanager
async def lifespan(app: FastAPI):
    # noqa: F401
    from models.post import posts  # noqa: F401

    # USAR A INSTÂNCIA 'database' PARA CONECTAR (Startup)
    await database.connect()
    metadata.create_all(engine)
    yield
    # USAR A INSTÂNCIA 'database' PARA DESCONECTAR (Shutdown)
    await database.disconnect()


tags_metadata = [
    {
        "name": "auth",
        "description": "Operações para autenticação e autorização.",
    },
    {
        "name": "users",
        "description": "Operações para manter Usuários na plataforma.",
    },
    {
        "name": "posts",
        "description": "Operações para manter Posts na plataforma.",
        "externalDocs": {
            "description": "Documentação externa para Post API.",
            "url": "https://fastapi.tiangolo.com/",
        },
    },
]

servers = [
    {"url": "https://desafio-dio-blog.onrender.com", "description": "Ambiente de Produção"},
    {"url": "http://localhost:8000", "description": "Ambiente de Desenvolvimento"},
]

app = FastAPI(
    # openapi_url = None, # Desabilitar as docOpenAPI e Redoc
    title="Capi-Blog API",
    version="0.4.0",
    summary="API assíncrona com FastAPI para gerenciamento de Blogs.",
    description="""
**_Capi-Blog API ajuda você a criar seu blog pessoal._**

## Posts

Você será capaz de fazer:

* **Criar posts**.
* **Recuperar posts**.
* **Recuperar posts por ID**.
* **Atualizar posts**.
* **Excluir posts**.
* **Limitar quantidade de posts diários** (_not implemented_).""",
    openapi_tags=tags_metadata,
    servers=servers,
    redoc_url="/redoc",  # None para Desabilitar a documentação Redoc
    docs_url="/docs",  # Habilitar a documentação Swagger UI
    lifespan=lifespan,
)

# Configuração de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas as origens
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],  # Permite todos os cabeçalhos
)


@app.exception_handler(NotFoundPostError)
async def not_found_post_error_handler(request: Request, exc: NotFoundPostError):
    return JSONResponse(status_code=404, content={"detail": exc.message})


@app.exception_handler(NotFoundUserError)
async def not_found_user_error_handler(request: Request, exc: NotFoundUserError):
    return JSONResponse(status_code=404, content={"detail": exc.message})


@app.exception_handler(BadRequestError)
async def bad_request_error_handler(request: Request, exc: BadRequestError):
    return JSONResponse(status_code=400, content={"detail": exc.message})


@app.exception_handler(ConflictError)
async def conflict_error_handler(request: Request, exc: ConflictError):
    return JSONResponse(status_code=409, content={"detail": exc.message})


app.include_router(auth.auth_router, tags=["auth"])
app.include_router(post.user_router, tags=["users"])
app.include_router(post.post_router, tags=["posts"])

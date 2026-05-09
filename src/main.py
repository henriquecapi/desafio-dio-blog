from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from controllers import auth, post
from database import database, engine, metadata
from exceptions import BadRequestError, ConflictError, NotFoundPostError, NotFoundUserError


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


app = FastAPI(lifespan=lifespan)


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


app.include_router(auth.auth_router)
app.include_router(post.user_router)
app.include_router(post.post_router)

from contextlib import asynccontextmanager

from fastapi import FastAPI

from controllers import auth, post
from database import database, engine, metadata


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
app.include_router(auth.auth_router)
app.include_router(post.user_router)
app.include_router(post.post_router)

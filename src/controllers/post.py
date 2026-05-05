from fastapi import APIRouter, Depends, status

from schemas.post import PostIn, PostUpdate, UserIn
from security import login_required
from services.post import PostService
from views.post import PostOut, UserOut

user_router = APIRouter(
    prefix="/users", dependencies=[Depends(login_required)], tags=["users"]
)
post_router = APIRouter(
    prefix="/posts", dependencies=[Depends(login_required)], tags=["blog-posts"]
)

service = PostService()


# USERS: ---------------------------------------------------------------------------
@user_router.post(
    "/",
    summary="Criar um novo Usuário",
    status_code=status.HTTP_201_CREATED,
    response_model=UserOut,
)
async def create_user(user: UserIn):
    return await service.create_user(user)


@user_router.delete(
    "/{id}",
    summary="Deletar um Usuário",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_user(id: int):
    await service.delete_user(id)
    return None


@user_router.get("/", summary="Selecionar todos usuários", response_model=list[UserOut])
async def read_users():
    return await service.read_users()


@user_router.get(
    "/email/{email}",
    summary="Selecionar usuário por e-mail",
    response_model=list[UserOut],
)
async def read_user_by_email(email: str):
    return await service.read_user_by_email(email)


@user_router.get("/{id}", summary="Selecionar Usuário por id", response_model=UserOut)
async def read_user_by_id(id: int):
    return await service.read_user_by_id(id)


# POSTS: ---------------------------------------------------------------------------
@post_router.get("/", summary="Listar todos os Posts", response_model=list[PostOut])
async def read_posts(pag: int = 1):
    return await service.read_posts(pag=pag)


@post_router.post(
    "/",
    summary="Criar um novo Post",
    status_code=status.HTTP_201_CREATED,
    response_model=PostOut,
)
async def create_post(post: PostIn):
    return await service.create_post(post)


@post_router.patch(
    "/{id}",
    summary="Atualizar um Post",
    status_code=status.HTTP_200_OK,
    response_model=PostOut,
)
async def update_post(id: int, post: PostUpdate):
    return await service.update_post(id, post)


@post_router.patch(
    "/published/{id}",
    summary="Publicar um Post",
    status_code=status.HTTP_200_OK,
    response_model=PostOut,
)
async def published(id: int):
    return await service.published(id)


@post_router.delete(
    "/{id}",
    summary="Deletar um Post",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_post(id: int):
    await service.delete_post(id)
    return None

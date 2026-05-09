from fastapi import APIRouter, Depends, status

from schemas.post import PostIn, PostUpdate, UserIn
from security import login_required
from services.post import PostService
from views.post import PostOut, UserOut

user_router = APIRouter(prefix="/users", dependencies=[Depends(login_required)])
post_router = APIRouter(prefix="/posts", dependencies=[Depends(login_required)])

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
async def get_users(id: int | None = None):
    return await service.get_users(id=id)


@user_router.get(
    "/email/{email}",
    summary="Selecionar usuário por e-mail",
    response_model=list[UserOut],
)
async def get_user_by_email(email: str):
    return await service.get_user_by_email(email)


@user_router.get("/{id}", summary="Selecionar Usuário por id", response_model=UserOut)
async def get_user_by_id(id: int):
    return await service.get_user_by_id(id)


# POSTS: ---------------------------------------------------------------------------
@post_router.get("/", summary="Listar todos os Posts", response_model=list[PostOut])
async def get_posts(pag: int = 1, published: bool | None = None, id: int | None = None):
    return await service.get_posts(pag=pag, published=published, id=id)


@post_router.get("/{id}", summary="Selecionar Post por id", response_model=PostOut)
async def get_post_by_id(id: int):
    return await service.get_post_by_id(id)


@post_router.get(
    "/title/{title}",
    summary="Selecionar posts por título",
    response_model=list[PostOut],
)
async def get_posts_by_title(title: str):
    return await service.get_posts_by_title(title)


@post_router.get(
    "/content/{content}",
    summary="Selecionar posts por conteúdo",
    response_model=list[PostOut],
)
async def get_posts_by_content(content: str):
    return await service.get_posts_by_content(content)


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

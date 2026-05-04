from fastapi import APIRouter, status
from services.post import PostService
from schemas.post import PostIn, PostUpdate
from views.post import PostOut

router = APIRouter(prefix="/posts", tags=["blog-posts"])
service = PostService()

@router.get("/", summary="Listar todos os Posts", response_model=list[PostOut])
async def read_posts(pag: int = 1):
    return await service.read_posts(pag=pag)

@router.post(
    "/",
    summary="Criar um novo Post",
    status_code=status.HTTP_201_CREATED,
    response_model=PostOut,
)
async def create_post(post: PostIn):
    return await service.create_post(post)

@router.patch(
    "/{id}",
    summary="Atualizar um Post",
    status_code=status.HTTP_200_OK,
    response_model=PostOut,
)
async def update_post(id: int, post: PostUpdate):
    return await service.update_post(id, post)

@router.patch(
    "/published/{id}",
    summary="Publicar um Post",
    status_code=status.HTTP_200_OK,
    response_model=PostOut,
)
async def published(id: int):
    return await service.published(id)

@router.delete(
    "/{id}",
    summary="Deletar um Post",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_post(id: int):
    await service.delete_post(id)
    return None
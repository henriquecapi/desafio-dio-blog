from datetime import datetime
from fastapi import HTTPException, status
from databases.interfaces import Record

from database import database
from models.post import posts
from schemas.post import PostIn, PostUpdate

class PostService:
    async def read_posts(self, pag: int = 1) -> list[Record]:
        limit = 3
        offset = (pag - 1) * limit
        query = posts.select().limit(limit).offset(offset)
        return await database.fetch_all(query)

    async def create_post(self, post: PostIn) -> Record:
        # Validação de campos obrigatórios
        if not post.title:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="O título é obrigatório.")
        if not post.content:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="O conteúdo é obrigatório.")

        query = posts.insert().values(
            title=post.title,
            content=post.content,
            published_at=datetime.now(),
            published=False,
        )
        last_id = await database.execute(query)
        
        # Retornamos o registro completo
        return await database.fetch_one(posts.select().where(posts.c.id == last_id))

    async def update_post(self, id: int, post: PostUpdate) -> Record:
        update_data = post.model_dump(exclude_unset=True)
        if not update_data:
            raise HTTPException(status_code=400, detail="Nenhum campo informado para atualização.")

        update_data["published_at"] = datetime.now()
        update_data["published"] = False

        query = posts.update().where(posts.c.id == id).values(**update_data)
        await database.execute(query)

        updated_post = await database.fetch_one(posts.select().where(posts.c.id == id))
        if not updated_post:
            raise HTTPException(status_code=404, detail="Post não encontrado.")
        
        return updated_post

    async def published(self, id: int) -> Record:
        query = posts.update().where(posts.c.id == id).values(
            published_at=datetime.now(),
            published=True,
        )
        await database.execute(query)

        updated_post = await database.fetch_one(posts.select().where(posts.c.id == id))
        if not updated_post:
            raise HTTPException(status_code=404, detail="Post não encontrado.")
        
        return updated_post

    async def delete_post(self, id: int) -> None:
        # Verifica existência
        post = await database.fetch_one(posts.select().where(posts.c.id == id))
        if not post:
            raise HTTPException(status_code=404, detail="Post não encontrado.")

        query = posts.delete().where(posts.c.id == id)
        await database.execute(query)

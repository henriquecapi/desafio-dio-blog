from datetime import datetime

from databases.interfaces import Record
from fastapi import HTTPException, status

from database import database
from models.post import posts, users
from schemas.post import PostIn, PostUpdate, UserIn


class PostService:
    # USERS: ---------------------------------------------------------------------------
    # async def login(user: UserIn) -> Record:
    #     query = users.select().where(users.c.email == user.email)
    #     user = await database.fetch_one(query)
    #     if not user:
    #         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email ou senha incorretos.")
    #     if user.senha != user.senha:
    #         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email ou senha incorretos.")
    #     return user
    async def create_user(self, user: UserIn) -> Record:
        query = users.insert().values(
            email=user.email,
            senha=user.senha,
            created_at=datetime.now(),
            token="",
            updated_at=datetime.now(),
        )
        last_id = await database.execute(query)
        return await database.fetch_one(users.select().where(users.c.id == last_id))

    async def delete_user(self, id: int) -> None:
        # Verifica existência
        user = await database.fetch_one(users.select().where(users.c.id == id))
        if not user:
            raise HTTPException(status_code=404, detail="Usuário não encontrado.")

        query = users.delete().where(users.c.id == id)
        await database.execute(query)

    async def read_users(self) -> list[Record]:
        query = users.select()
        return await database.fetch_all(query)

    async def read_user_by_email(self, email: str) -> list[Record]:
        query = users.select().where(users.c.email.like(f"%{email}%"))
        return await database.fetch_all(query)

    async def read_user_by_id(self, id: int) -> Record:
        query = users.select().where(users.c.id == id)
        user = await database.fetch_one(query)
        if not user:
            raise HTTPException(status_code=404, detail="Usuário não encontrado.")
        return user

    # POSTS: ---------------------------------------------------------------------------
    async def read_posts(self, pag: int = 1) -> list[Record]:
        limit = 3
        offset = (pag - 1) * limit
        query = posts.select().limit(limit).offset(offset)
        return await database.fetch_all(query)

    async def create_post(self, post: PostIn) -> Record:
        # Validação de campos obrigatórios
        if not post.title:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="O título é obrigatório.",
            )
        if not post.content:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="O conteúdo é obrigatório.",
            )

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
            raise HTTPException(
                status_code=400,
                detail="Nenhum campo informado para atualização.",
            )

        update_data["published_at"] = datetime.now()
        update_data["published"] = False

        query = posts.update().where(posts.c.id == id).values(**update_data)
        await database.execute(query)

        updated_post = await database.fetch_one(posts.select().where(posts.c.id == id))
        if not updated_post:
            raise HTTPException(status_code=404, detail="Post não encontrado.")

        return updated_post

    async def published(self, id: int) -> Record:
        query = (
            posts.update()
            .where(posts.c.id == id)
            .values(
                published_at=datetime.now(),
                published=True,
            )
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

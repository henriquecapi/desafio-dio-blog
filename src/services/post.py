from datetime import datetime
from typing import cast

from databases.interfaces import Record

from database import database
from exceptions import (BadRequestError, ConflictError, NotFoundPostError,
                        NotFoundUserError)
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
        # Verifica se já existe
        query = users.select().where(users.c.email == user.email)
        if await database.fetch_one(query):
            raise ConflictError("Já existe um usuário com este e-mail.")

        query = users.insert().values(
            email=user.email,
            senha=user.senha,
            created_at=datetime.now(),
            token="",
            updated_at=datetime.now(),
        )
        last_id = await database.execute(query)
        return cast(
            Record, await database.fetch_one(users.select().where(users.c.id == last_id))
        )

    async def delete_user(self, id: int) -> None:
        # Verifica existência
        user = await database.fetch_one(users.select().where(users.c.id == id))
        if not user:
            raise NotFoundUserError()

        query = users.delete().where(users.c.id == id)
        await database.execute(query)

    async def get_users(self, id: int | None = None) -> list[Record]:
        query = users.select()
        if id is not None:
            query = query.where(users.c.id == id)
        return await database.fetch_all(query)

    async def get_user_by_email(self, email: str) -> list[Record]:
        query = users.select().where(users.c.email.like(f"%{email}%"))
        return await database.fetch_all(query)

    async def get_user_by_id(self, id: int) -> Record:
        query = users.select().where(users.c.id == id)
        user = await database.fetch_one(query)
        if not user:
            raise NotFoundUserError()
        return user

    # POSTS: ---------------------------------------------------------------------------
    async def get_posts(
        self, pag: int = 1, published: bool | None = None, id: int | None = None
    ) -> list[Record]:
        limit = 5
        offset = (pag - 1) * limit
        query = posts.select()

        if published is not None:
            query = query.where(posts.c.published == published)

        if id is not None:
            query = query.where(posts.c.id == id)
        # Se não informado, retorna todos (True + False)

        query = query.limit(limit).offset(offset)
        return await database.fetch_all(query)

    async def get_post_by_id(self, id: int) -> Record:
        query = posts.select().where(posts.c.id == id)
        post = await database.fetch_one(query)
        if not post:
            raise NotFoundPostError()
        return post

    async def get_posts_by_title(self, title: str) -> list[Record]:
        query = posts.select().where(posts.c.title.like(f"%{title}%"))
        return await database.fetch_all(query)

    async def get_posts_by_content(self, content: str) -> list[Record]:
        query = posts.select().where(posts.c.content.like(f"%{content}%"))
        return await database.fetch_all(query)

    async def create_post(self, post: PostIn) -> Record:
        # Validação de campos obrigatórios
        if not post.title:
            raise BadRequestError("O título é obrigatório.")
        if not post.content:
            raise BadRequestError("O conteúdo é obrigatório.")

        # Verifica se já existe post com o mesmo título
        query = posts.select().where(posts.c.title == post.title)
        if await database.fetch_one(query):
            raise ConflictError("Já existe um post com este título.")

        query = posts.insert().values(
            title=post.title,
            content=post.content,
            published_at=datetime.now(),
            published=False,
        )
        last_id = await database.execute(query)

        # Retornamos o registro completo
        return cast(
            Record, await database.fetch_one(posts.select().where(posts.c.id == last_id))
        )

    async def update_post(self, id: int, post: PostUpdate) -> Record:
        update_data = post.model_dump(exclude_unset=True)
        if not update_data:
            raise BadRequestError("Nenhum campo informado para atualização.")

        # Se estiver atualizando o título, verifica se já existe
        if post.title:
            query = posts.select().where(posts.c.title == post.title, posts.c.id != id)
            if await database.fetch_one(query):
                raise ConflictError("Já existe um post com este título.")

        update_data["published_at"] = datetime.now()
        update_data["published"] = False

        query = posts.update().where(posts.c.id == id).values(**update_data)
        await database.execute(query)

        updated_post = await database.fetch_one(posts.select().where(posts.c.id == id))
        if not updated_post:
            raise NotFoundPostError()

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
            raise NotFoundPostError()

        return updated_post

    async def delete_post(self, id: int) -> None:
        # Verifica existência
        post = await database.fetch_one(posts.select().where(posts.c.id == id))
        if not post:
            raise NotFoundPostError()

        query = posts.delete().where(posts.c.id == id)
        await database.execute(query)

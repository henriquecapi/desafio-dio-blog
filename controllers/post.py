from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Cookie, Header, Response, status
from schemas.post import Foo, PostIn
from views.post import PostOut

router = APIRouter(prefix="/posts")

fake_db = [
    {
        "title": "Criando uma aplicação com Django",
        "date": datetime.now(),
        "published": True,
    },
    {
        "title": "Internacionalizando uma app FastAPI",
        "date": datetime.now(),
        "published": False,
    },
    {
        "title": "Criando uma aplicação com Flask",
        "date": datetime.now(),
        "published": True,
    },
    {
        "title": "Internacionalizando uma app Starlette",
        "date": datetime.now(),
        "published": True,
    },
]


@router.get("/foobar", response_model=Foo)
def foobar() -> dict[str, str]:
    return {"bar": "foo", "message": "Hello World"}


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostOut)
def create_post(post: PostIn):
    fake_db.append(post.model_dump())
    return post


@router.get("/", response_model=list[PostOut])
def read_posts(
    response: Response,
    published: bool = False,
    limit: int | None = None,
    skip: int = 0,
    ads_id: Annotated[str | None, Cookie()] = None,
    user_agent: Annotated[str | None, Header()] = None,
):
    email = "teste@hotmail.com"
    response.set_cookie(key="user", value=email)
    print(f"Cookie: {ads_id}")
    print(f"User Agent: {user_agent}")
    print(f"Email: {email}")

    if limit is None:
        limit = len(fake_db)

    filtered = [post for post in fake_db if post["published"] is published]
    return filtered[skip : skip + limit]


@router.get("/{framework}", response_model=list[PostOut])
def read_framework_posts(framework: str):
    return [
        {
            "title": f"Criando uma aplicação com {framework}",
            "date": datetime.now(),
            "published": True,
        },
        {
            "title": f"Internacionalizando uma app {framework}",
            "date": datetime.now(),
            "published": True,
        },
    ]

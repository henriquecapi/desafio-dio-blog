from datetime import datetime

from pydantic import BaseModel


class PostIn(BaseModel):
    title: str | None = None
    content: str | None = None


class PostUpdate(BaseModel):
    title: str | None = None
    content: str | None = None


class UserIn(BaseModel):
    email: str
    senha: str

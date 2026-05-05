from datetime import datetime

from pydantic import BaseModel


class PostOut(BaseModel):
    id: int
    title: str
    content: str
    published_at: datetime | None
    published: bool


class UserOut(BaseModel):
    id: int
    email: str
    token: str | None
    updated_at: datetime | None
    created_at: datetime | None

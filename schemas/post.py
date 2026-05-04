from datetime import datetime

from pydantic import BaseModel


class PostIn(BaseModel):
    title: str
    date: datetime = datetime.now()
    published: bool = False


class Foo(BaseModel):
    bar: str
    message: str

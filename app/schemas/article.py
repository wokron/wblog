from datetime import datetime
from pydantic import BaseModel, Field
from . import tag, comment, category


class Article(BaseModel):
    id: int = Field(gt=0)
    title: str = Field(min_length=1, max_length=50)
    content: str = ""
    create_time: datetime
    update_time: datetime
    is_deleted: bool = False
    comments: list[comment.Comment] = []
    category: category.Category = None
    tags: list[tag.Tag] = []

    class Config:
        orm_mode = True


class ArticleCreate(BaseModel):
    title: str = Field(min_length=1, max_length=50)
    content: str = ""


class ArticleUpdate(BaseModel):
    title: str = Field(None, min_length=1, max_length=50)
    content: str = None
    is_deleted: bool = None

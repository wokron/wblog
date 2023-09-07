from datetime import datetime
from pydantic import BaseModel
from . import tag, comment, category


class ArticleBase(BaseModel):
    title: str
    content: str


class Article(ArticleBase):
    id: int
    create_time: datetime
    update_time: datetime
    is_deleted: bool
    comments: list[comment.Comment]
    category: category.Category
    tags: list[tag.Tag]

    class Config:
        orm_mode = True


class ArticleCreate(ArticleBase):
    pass


class ArticleModify(ArticleBase):
    is_deleted: bool

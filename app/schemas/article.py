from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from . import tag, comment
from .category import Category


class WriterInfo(BaseModel):
    id: int = Field(gt=0)
    name: str = Field(min_length=1, max_length=20)


class Article(BaseModel):
    id: int = Field(gt=0)
    title: str = Field(min_length=1, max_length=50)
    content: str = ""
    create_time: datetime
    update_time: datetime
    is_deleted: bool = False
    category: Category | None = None
    tags: list[tag.Tag] = []
    writer: WriterInfo

    model_config = ConfigDict(from_attributes=True)


class ArticleSimplify(BaseModel):
    id: int = Field(gt=0)
    title: str = Field(min_length=1, max_length=50)
    create_time: datetime
    update_time: datetime
    is_deleted: bool = False
    category: Category | None = None
    tags: list[tag.Tag] = []
    writer: WriterInfo

    model_config = ConfigDict(from_attributes=True)


class ArticleCreate(BaseModel):
    title: str = Field(min_length=1, max_length=50)
    content: str = ""
    tags: list[str] = []
    category: str | None = Field(None, min_length=1, max_length=20)


class ArticleUpdate(BaseModel):
    title: str = Field(None, min_length=1, max_length=50)
    content: str = None
    is_deleted: bool = None

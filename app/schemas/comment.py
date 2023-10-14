from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from . import member


class ArticleForComment(BaseModel):
    id: int = Field(gt=0)
    title: str = Field(min_length=1, max_length=50)


class Comment(BaseModel):
    id: int = Field(gt=0)
    content: str = Field(max_length=250)
    commenter_name: str | None = Field(max_length=20)
    like: int = Field(ge=0)
    dislike: int = Field(ge=0)
    create_time: datetime
    member: member.Member | None
    article: ArticleForComment

    model_config = ConfigDict(from_attributes=True)


class CommentCreate(BaseModel):
    content: str = Field(max_length=250)
    commenter_name: str | None = Field(None, max_length=20)


class CommentUpdate(BaseModel):
    content: str = Field(None, max_length=250)

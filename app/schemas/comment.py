from datetime import datetime
from pydantic import BaseModel, Field
from . import member


class Comment(BaseModel):
    id: int = Field(gt=0)
    content: str = Field(max_length=250)
    commenter_name: str | None = Field(max_length=20)
    like: int = Field(ge=0)
    dislike: int = Field(ge=0)
    create_time: datetime
    member: member.Member | None

    class Config:
        orm_mode = True


class CommentCreate(BaseModel):
    content: str = Field(max_length=250)
    commenter_name: str | None = Field(None, max_length=20)


class CommentUpdate(BaseModel):
    content: str = Field(None, max_length=250)
    add_like: bool = None
    add_dislike: bool = None

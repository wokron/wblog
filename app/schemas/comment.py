from datetime import datetime
from pydantic import BaseModel
from . import member


class CommentBase(BaseModel):
    content: str
    commenter_name: str | None


class Comment(CommentBase):
    id: int
    like: int
    dislike: int
    create_time: datetime
    member: member.Member | None

    class Config:
        orm_mode = True


class CommentCreate(CommentBase):
    pass

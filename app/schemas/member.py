from pydantic import BaseModel
from ..models.member import Role


class MemberBase(BaseModel):
    name: str
    role: Role


class Member(MemberBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True


class MemberCreate(MemberBase):
    password: str


class MemberModify(MemberBase):
    password: str
    is_active: bool

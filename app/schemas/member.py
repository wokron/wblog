from pydantic import BaseModel, ConfigDict, Field
from ..models.member import Role


class Member(BaseModel):
    id: int = Field(gt=0)
    name: str = Field(min_length=1, max_length=20)
    role: Role
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class MemberCreate(BaseModel):
    name: str = Field(min_length=1, max_length=20)
    role: Role = Role.MEMBER
    password: str = Field(min_length=8, max_length=24, pattern="^[0-9a-zA-Z]+$")


class MemberUpdate(BaseModel):
    name: str = Field(None, min_length=1, max_length=20)
    role: Role = None
    password: str = Field(None, min_length=8, max_length=24, pattern="^[0-9a-zA-Z]+$")
    is_active: bool = None

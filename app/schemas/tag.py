from pydantic import BaseModel


class TagBase(BaseModel):
    name: str


class Tag(TagBase):
    id: int

    class Config:
        orm_mode = True


class TagCreate(TagBase):
    pass

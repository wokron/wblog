from pydantic import BaseModel, Field


class TagBase(BaseModel):
    name: str = Field(min_length=1, max_length=20)


class Tag(TagBase):
    id: int = Field(gt=0)

    class Config:
        orm_mode = True


class TagCreate(TagBase):
    pass

from pydantic import BaseModel, ConfigDict, Field


class TagBase(BaseModel):
    name: str = Field(min_length=1, max_length=20)


class Tag(TagBase):
    id: int = Field(gt=0)

    model_config = ConfigDict(from_attributes=True)


class TagCreate(TagBase):
    pass

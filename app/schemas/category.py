from pydantic import BaseModel, Field


class CategoryBase(BaseModel):
    name: str = Field(min_length=1, max_length=20)


class Category(CategoryBase):
    id: int = Field(gt=0)

    class Config:
        orm_mode = True


class CategoryCreate(CategoryBase):
    pass

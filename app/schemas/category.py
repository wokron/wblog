from pydantic import BaseModel


class CategoryBase(BaseModel):
    name: str


class Category(CategoryBase):
    id: int

    class Config:
        orm_mode = True


class CategoryCreate(CategoryBase):
    pass

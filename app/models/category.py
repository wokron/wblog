from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from ..core.database import Base


class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String, nullable=False, unique=True)

    articles = relationship("Article", back_populates="category")

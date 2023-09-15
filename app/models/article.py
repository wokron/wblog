from datetime import datetime
from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    Text,
    DateTime,
    Table,
)
from sqlalchemy.orm import relationship

from ..core.database import Base

article2tag = Table(
    "article2tag",
    Base.metadata,
    Column("article_id", ForeignKey("article.id"), primary_key=True),
    Column("tag_id", ForeignKey("tag.id"), primary_key=True),
)


class Article(Base):
    __tablename__ = "article"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    title = Column(String, nullable=False, unique=True)
    content = Column(Text, nullable=False, default="")
    create_time = Column(DateTime, nullable=False, default=datetime.now)
    update_time = Column(
        DateTime, nullable=False, default=datetime.now, onupdate=datetime.now
    )
    is_deleted = Column(Boolean, nullable=False, default=False)

    category_id = Column(Integer, ForeignKey("category.id"))
    writer_id = Column(Integer, ForeignKey("member.id"))

    writer = relationship("Member", back_populates="articles")
    comments = relationship("Comment", back_populates="article", cascade="all, delete")
    category = relationship("Category", back_populates="articles")
    tags = relationship("Tag", secondary="article2tag", back_populates="articles")

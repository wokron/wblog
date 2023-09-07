import enum
from sqlalchemy import Boolean, Column, Integer, String, Enum
from sqlalchemy.orm import relationship

from ..core.database import Base


class Role(enum.Enum):
    CREATER = "Creator"
    MANAGER = "Manager"
    MEMBER = "Common Member"


class Member(Base):
    __tablename__ = "member"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(Role), nullable=False, default=Role.MEMBER)
    is_active = Column(Boolean, nullable=False, default=True)

    articles = relationship(
        "Article", secondary="article2member", back_populates="writers"
    )
    comments = relationship("Comment", back_populates="member")

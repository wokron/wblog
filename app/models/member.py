import enum
from sqlalchemy import Boolean, Column, Integer, String, Enum, event
from sqlalchemy.orm import relationship
from ..dependencies import config
from ..utils import get_password_hash

from ..core.database import Base


class Role(enum.Enum):
    OWNER = "Owner"
    MANAGER = "Manager"
    MEMBER = "Common Member"


class Member(Base):
    __tablename__ = "member"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(Role), nullable=False, default=Role.MEMBER)
    is_active = Column(Boolean, nullable=False, default=True)

    articles = relationship("Article", back_populates="writer")
    comments = relationship("Comment", back_populates="member")


def create_owner_data(target, connection, **kw):
    settings = config.get_settings()
    connection.execute(
        target.insert(),
        {
            "name": settings.owner_name,
            "hashed_password": get_password_hash(settings.owner_password),
            "role": Role.OWNER,
        },
    )


event.listen(Member.__table__, "after_create", create_owner_data)

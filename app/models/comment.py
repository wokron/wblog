from datetime import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from ..database import Base


class Comment(Base):
    __tablename__ = "comment"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    content = Column(String, nullable=False)
    commenter_name = Column(String, nullable=True, default=None)
    like = Column(Integer, nullable=False, default=0)
    dislike = Column(Integer, nullable=False, default=0)
    create_time = Column(DateTime, nullable=False, default=datetime.now)

    article_id = Column(Integer, ForeignKey("article.id"))
    member_id = Column(Integer, ForeignKey("member.id"), nullable=True)

    article = relationship("Article", back_populates="comments")
    member = relationship("Member", back_populates="comments")

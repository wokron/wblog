from datetime import datetime
from sqlalchemy import desc, func
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from .. import models
from .. import schemas
from . import get_article


def get_comment(db: Session, comment_id: int):
    return db.query(models.Comment).filter(models.Comment.id == comment_id).first()


def list_comments(
    db: Session,
    article_id: int,
    order_by: str = "-create_time",
    skip: int = 0,
    limit: int = 10,
):
    article = get_article(db, article_id)
    if article is None:
        return []

    query = article.comments.offset(skip).limit(limit)
    if order_by is not None:
        if order_by.startswith("-"):
            order_by = order_by[1:]
            query = query.order_by(desc(order_by))
        else:
            query = query.order_by(order_by)
    return query.all()


def create_comment(db: Session, article_id: int, comment: schemas.CommentCreate):
    try:
        db_comment = models.Comment(**comment.model_dump(), article_id=article_id)
        db.add(db_comment)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        return None
    db.refresh(db_comment)
    return db_comment


def delete_comment(db: Session, comment_id: int):
    try:
        db.query(models.Comment).filter(models.Comment.id == comment_id).delete()
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        return False
    return True


def update_comment(db: Session, comment_id: int, comment: schemas.CommentUpdate):
    comment_to_update = get_comment(db, comment_id)
    if comment_to_update is None:
        return True

    try:
        if comment.add_like is not None:
            comment_to_update.like += 1
        if comment.add_dislike is not None:
            comment_to_update.dislike += 1
        if comment.content is not None:
            comment_to_update.content = comment.content
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        return False
    return True

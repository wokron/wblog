from datetime import datetime
from sqlalchemy import desc, func
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from .. import models
from .. import schemas


def get_article(db: Session, article_id: int):
    return db.query(models.Article).filter(models.Article.id == article_id).first()


def get_article_by_title(db: Session, article_title: str):
    return (
        db.query(models.Article).filter(models.Article.title == article_title).first()
    )


def list_articles(
    db: Session,
    title_like: str = None,
    content_has: str = None,
    category_id: int = None,
    tag_ids: list[int] = None,
    writer_ids: list[int] = None,
    create_time_after: datetime = None,
    create_time_before: datetime = None,
    update_time_after: datetime = None,
    update_time_before: datetime = None,
    is_deleted: bool = None,
    order_by: str = "-create_time",
):
    params = []
    if title_like is not None:
        params.append(models.Article.title.like(f"%{title_like}%"))
    if content_has is not None:
        params.append(models.Article.content.like(f"%{content_has}%"))
    if category_id is not None:
        params.append(models.Article.category_id == category_id)
    if tag_ids is not None:
        article_ids_with_all_tags = (
            db.query(models.article2tag.c.article_id)
            .filter(models.article2tag.c.tag_id.in_(tag_ids))
            .group_by(models.article2tag.c.article_id)
            .having(func.count(models.article2tag.c.tag_id) == len(tag_ids))
        )
        params.append(models.Article.id.in_(article_ids_with_all_tags))
    if writer_ids is not None:
        article_ids_with_all_writers = (
            db.query(models.article2member.c.article_id)
            .filter(models.article2member.c.member_id.in_(writer_ids))
            .group_by(models.article2member.c.article_id)
            .having(func.count(models.article2member.c.member_id) == len(writer_ids))
        )
        params.append(models.Article.id.in_(article_ids_with_all_writers))
    if create_time_after is not None:
        params.append(models.Article.create_time > create_time_after)
    if create_time_before is not None:
        params.append(models.Article.create_time < create_time_before)
    if update_time_after is not None:
        params.append(models.Article.update_time > update_time_after)
    if update_time_before is not None:
        params.append(models.Article.update_time < update_time_after)
    if is_deleted is not None:
        params.append(models.Article.is_deleted == is_deleted)

    query = db.query(models.Article).filter(*params)

    if order_by is not None:
        if order_by.startswith("-"):
            order_by = order_by[1:]
            query = query.order_by(desc(order_by))
        else:
            query = query.order_by(order_by)

    return query.all()


def create_article(db: Session, article: schemas.ArticleCreate):
    try:
        db_article = models.Article(**article.model_dump())
        db.add(db_article)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        return None
    db.refresh(db_article)
    return db_article


def delete_article(db: Session, article_id: int):
    try:
        db.query(models.Article).filter(models.Article.id == article_id).delete()
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        return False
    return True


def update_article(db: Session, article_id: int, article: schemas.ArticleUpdate):
    try:
        db.query(models.Article).filter(models.Article.id == article_id).update(
            article.model_dump(exclude_unset=True)
        )
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        return False
    return True

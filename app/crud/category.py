from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from .. import models
from .. import schemas


def get_category(db: Session, category_id: int):
    return db.query(models.Category).filter(models.Category.id == category_id).first()


def get_category_by_name(db: Session, category_name: str):
    return (
        db.query(models.Category).filter(models.Category.name == category_name).first()
    )


def list_categorys(db: Session, hide_unused: bool = False):
    params = []
    if hide_unused:
        category_ids = db.query(models.Article.category_id)
        params.append(models.Category.id.in_(category_ids))

    return db.query(models.Category).filter(*params).all()


def create_category(db: Session, category: schemas.CategoryCreate):
    try:
        db_category = models.Category(**category)
        db.add(db_category)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        return None
    db.refresh(db_category)
    return db_category


def delete_category(db: Session, category_id: int):
    try:
        db.query(models.Category).filter(models.Category.id == category_id).delete()
    except SQLAlchemyError as e:
        db.rollback()
        return False
    return True

def set_article_category(db: Session, category_id: int, article_id: int):
    try:
        db.query(models.Article).filter(models.Article.id == article_id).update(
            {"category_id": category_id}
        )
    except SQLAlchemyError as e:
        db.rollback()
        return False
    return True

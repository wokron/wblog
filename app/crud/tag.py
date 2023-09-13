from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from .. import models
from .. import schemas


def get_tag(db: Session, tag_id: int):
    return db.query(models.Tag).filter(models.Tag.id == tag_id).first()


def get_tag_by_name(db: Session, tag_name: str):
    return db.query(models.Tag).filter(models.Tag.name == tag_name).first()


def list_tags(db: Session, hide_unused: bool = False):
    params = []
    if hide_unused:
        tag_ids = db.query(models.article2tag.c.tag_id)
        params.append(models.Tag.id.in_(tag_ids))
    return db.query(models.Tag).filter(*params).all()


def create_tag(db: Session, tag: schemas.TagCreate):
    try:
        db_tag = models.Tag(**tag.model_dump())
        db.add(db_tag)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        return None
    db.refresh(db_tag)
    return db_tag


def delete_tag(db: Session, tag_id: int):
    try:
        db.query(models.Tag).filter(models.Tag.id == tag_id).delete()
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        return False
    return True

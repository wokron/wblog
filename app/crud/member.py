from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from .. import models
from .. import schemas


def get_member(db: Session, member_id: int):
    return db.query(models.Member).filter(models.Member.id == member_id).first()


def get_member_by_name(db: Session, member_name: str):
    return db.query(models.Member).filter(models.Member.name == member_name).first()


def list_members(
    db: Session,
    name_like: str = None,
    role: models.Role = None,
    is_active: bool = None,
    skip: int = 0,
    limit: int = 10,
):
    params = []
    if name_like:
        params.append(models.Member.name.like(f"%{name_like}%"))
    if role:
        params.append(models.Member.role == role)
    if is_active:
        params.append(models.Member.is_active == is_active)
    return db.query(models.Member).filter(*params).offset(skip).limit(limit).all()


def create_member(db: Session, member: schemas.MemberCreate):
    hashed_password = member.password + "fake hash"  # todo: need hash
    try:
        db_member = models.Member(
            **member.model_dump(exclude=["password"]), hashed_password=hashed_password
        )
        db.add(db_member)
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        return None

    db.refresh(db_member)
    return db_member


def update_member(db: Session, member_id: int, member: schemas.MemberUpdate):
    try:
        params = member.model_dump(exclude_unset=True, exclude=["password"])
        params.update(
            {"hashed_password": member.password + "fake hash"}
        )  # todo: need hash
        db.query(models.Member).filter(models.Member.id == member_id).update(params)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        return False
    return True

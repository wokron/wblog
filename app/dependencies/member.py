from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from .oauth2 import oauth2_scheme
from .database import get_db
from ..utils import jwt_decode
from .. import crud, models
import jwt

async def get_current_member(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt_decode(token)
    except jwt.ExpiredSignatureError as e:
        raise credentials_exception
    if payload is None:
        raise credentials_exception
    name: str = payload.get("sub")
    if name is None:
        raise credentials_exception
    user = crud.get_member_by_name(db, name)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_member(
    current_member: models.Member = Depends(get_current_member),
):
    if not current_member.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="member is inactive"
        )
    return current_member

from datetime import timedelta
from fastapi import APIRouter, Depends, Path, HTTPException, status, Body
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session
from .. import crud, schemas, models
from ..dependencies.database import get_db
from ..dependencies.config import get_settings
from ..config import Settings
from ..utils import create_token

router = APIRouter(
    prefix="/token",
    tags=["token"],
)


@router.post("/", response_model=schemas.Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
    setting: Settings = Depends(get_settings),
):
    member: models.Member = crud.authenticate_member(db, form_data.username, form_data.password)
    if member is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not member.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="login is forbiddened",
        )
    access_token_expires = timedelta(minutes=setting.access_token_expire_minutes)
    access_token = create_token(
        data={"sub": member.name}, expires_delta=access_token_expires
    )
    return schemas.Token(access_token=access_token, token_type="bearer")

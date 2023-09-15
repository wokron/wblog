from fastapi import APIRouter, Depends, Path, HTTPException, status, Body

from sqlalchemy.orm import Session
from ... import crud, schemas
from ...dependencies.database import get_db
from ...dependencies.member import get_current_active_member

router = APIRouter(
    prefix="/tag",
    tags=["tag"],
)


@router.get("/", response_model=list[schemas.Tag])
async def list_tags(hide_unused: bool = False, db: Session = Depends(get_db)):
    tags = crud.list_tags(db, hide_unused)
    return tags


@router.get("/{tag_id}", response_model=schemas.Tag)
async def get_tag(tag_id: int = Path(gt=0), db: Session = Depends(get_db)):
    result_tag = crud.get_tag(db, tag_id)
    if result_tag is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="tag not found"
        )
    return result_tag


@router.post(
    "/",
    response_model=schemas.Tag,
    dependencies=[Depends(get_current_active_member)],
)
async def create_tag(tag: schemas.TagCreate, db: Session = Depends(get_db)):
    if crud.get_tag_by_name(db, tag.name) is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="tag already exist"
        )
    tag_created = crud.create_tag(db, tag)
    if tag_created is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="fail to create tag"
        )
    return tag_created


@router.delete("/{tag_id}", dependencies=[Depends(get_current_active_member)])
async def delete_tag(tag_id: int = Path(gt=0), db: Session = Depends(get_db)):
    success = crud.delete_tag(db, tag_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="fail to delete tag"
        )

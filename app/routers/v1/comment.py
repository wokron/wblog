from datetime import datetime
from fastapi import APIRouter, Depends, Path, HTTPException, Query, status, Body

from sqlalchemy.orm import Session
from ... import crud, schemas
from ...dependencies.database import get_db

router = APIRouter(
    prefix="/comment",
    tags=["comment"],
)


@router.get("/{comment_id}", response_model=schemas.Comment)
def get_comment(comment_id: int = Path(gt=0), db: Session = Depends(get_db)):
    result_comment = crud.get_comment(db, comment_id)
    if result_comment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="comment not found"
        )
    return result_comment


@router.delete("/{comment_id}")
def delete_comment(comment_id: int = Path(gt=0), db: Session = Depends(get_db)):
    success = crud.delete_comment(db, comment_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="fail to delete comment"
        )


@router.patch("/{comment_id}")
def update_comment(
    comment: schemas.CommentUpdate,
    comment_id: int = Path(gt=0),
    db: Session = Depends(get_db),
):
    success = crud.update_comment(db, comment_id, comment)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="fail to update comment"
        )

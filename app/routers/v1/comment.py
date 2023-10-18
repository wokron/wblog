from fastapi import (
    APIRouter,
    Depends,
    Path,
    HTTPException,
    Query,
    Response,
    status,
)

from sqlalchemy.orm import Session
from ... import crud, schemas, models
from ...dependencies.database import get_db
from ...dependencies.member import get_current_active_member

router = APIRouter(
    prefix="/comment",
    tags=["comment"],
)


@router.get("/", response_model=list[schemas.Comment])
def list_comments(
    response: Response,
    article_id: int = Query(None, gt=0),
    member_id: int = Query(None, gt=0),
    order_by: str = Query("-create_time", pattern="^-?(create_time|like|dislike)$"),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, gt=0),
    db: Session = Depends(get_db),
):
    comments, total = crud.list_comments(db, article_id, member_id, order_by, skip, limit)
    response.headers["X-Total-Count"] = str(total)
    return comments


@router.get("/{comment_id}", response_model=schemas.Comment)
def get_comment(comment_id: int = Path(gt=0), db: Session = Depends(get_db)):
    result_comment = crud.get_comment(db, comment_id)
    if result_comment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="comment not found"
        )
    return result_comment


@router.delete("/{comment_id}")
def delete_comment(
    comment_id: int = Path(gt=0),
    db: Session = Depends(get_db),
    current_member: models.Member = Depends(get_current_active_member),
):
    comment = crud.get_comment(db, comment_id)
    if comment is None:
        return
    if (
        comment.article.writer_id != current_member.id
        and comment.member_id != current_member.id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="no permission to delete comment",
        )
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
    current_member: models.Member = Depends(get_current_active_member),
):
    comment_to_update = crud.get_comment(db, comment_id)
    if comment is None:
        return
    if (
        comment_to_update.member_id == None
        or comment_to_update.member_id != current_member.id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="no premission to update comment",
        )
    success = crud.update_comment(db, comment_id, comment)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="fail to update comment"
        )


@router.post("/{comment_id}/like")
def add_comment_like(
    comment_id: int = Path(gt=0),
    db: Session = Depends(get_db),
):
    success = crud.add_comment_like(db, comment_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="fail to add like of comment",
        )


@router.post("/{comment_id}/dislike")
def add_comment_dislike(
    comment_id: int = Path(gt=0),
    db: Session = Depends(get_db),
):
    success = crud.add_comment_dislike(db, comment_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="fail to add dislike of comment",
        )

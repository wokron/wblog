from datetime import datetime
from fastapi import APIRouter, Depends, Path, HTTPException, Query, status, Body, Response

from sqlalchemy.orm import Session
from ... import crud, schemas, models
from ...dependencies.database import get_db
from ...dependencies.member import get_current_active_member

router = APIRouter(
    prefix="/article",
    tags=["article"],
)


@router.get("/", response_model=list[schemas.ArticleSimplify])
async def list_articles(
    response: Response,
    title_like: str = Query(None, min_length=1, max_length=50),
    content_has: str = None,
    category_id: int = Query(None, gt=0),
    tag_ids: list[int] = Query(None),
    writer_id: int = Query(None, gt=0),
    create_time_after: datetime = None,
    create_time_before: datetime = None,
    update_time_after: datetime = None,
    update_time_before: datetime = None,
    is_deleted: bool = None,
    order_by: str = Query(
        "-create_time", pattern="^-?(create_time|update_time|title)$"
    ),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, gt=0),
    db: Session = Depends(get_db),
):
    articles, total = crud.list_articles(
        db,
        title_like,
        content_has,
        category_id,
        tag_ids,
        writer_id,
        create_time_after,
        create_time_before,
        update_time_after,
        update_time_before,
        is_deleted,
        order_by,
        skip,
        limit,
    )
    response.headers["X-Total-Count"] = str(total)
    return articles


@router.get("/{article_id}", response_model=schemas.Article)
async def get_article(article_id: int = Path(gt=0), db: Session = Depends(get_db)):
    result_article = crud.get_article(db, article_id)
    if result_article is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="article not found"
        )
    return result_article


@router.post("/", response_model=schemas.ArticleSimplify)
async def create_article(
    article: schemas.ArticleCreate,
    db: Session = Depends(get_db),
    current_member: models.Member = Depends(get_current_active_member),
):
    if crud.get_article_by_title(db, article.title) is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="article title already exist"
        )
    article_created = crud.create_article(db, current_member.id, article)
    if article_created is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="fail to create article"
        )
    return article_created


@router.delete("/{article_id}")
async def delete_article(
    article_id: int = Path(gt=0),
    db: Session = Depends(get_db),
    current_member: models.Member = Depends(get_current_active_member),
):
    article: models.Article = crud.get_article(db, article_id)
    if article is None:
        return  # no article to delete, so just return
    if not article.is_deleted:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="cannot delete article when is_delete=false",
        )
    if not (
        current_member.role == models.Role.OWNER
        or (
            current_member.role == models.Role.MANAGER
            and article.writer.role == models.Role.MEMBER
        )
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="no permission to delete article",
        )

    success = crud.delete_article(db, article_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="fail to delete article"
        )


@router.patch("/{article_id}")
async def update_article(
    article: schemas.ArticleUpdate,
    article_id: int = Path(gt=0),
    db: Session = Depends(get_db),
    current_member: models.Member = Depends(get_current_active_member),
):
    article_to_update: models.Article = crud.get_article(db, article_id)
    if article_to_update is None:
        return
    if article.is_deleted is not None:
        if article.title is not None or article.content is not None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="when is_deleted is set, title and content can not update at same time",
            )
        if current_member.id != article_to_update.writer_id and (
            article_to_update.writer.role == models.Role.OWNER
            or current_member.role == models.Role.MEMBER
            or (
                article_to_update.writer.role == models.Role.MANAGER
                and current_member.role == models.Role.MANAGER
            )
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="no premission to set is_deleted in article",
            )
    else:
        if current_member.id != article_to_update.writer_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="no premission to update article",
            )

    success = crud.update_article(db, article_id, article)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="fail to update article"
        )


@router.put("/{article_id}/category", tags=["category"])
async def set_article_category(
    category: schemas.CategoryWithName,
    article_id: int = Path(gt=0),
    db: Session = Depends(get_db),
    current_member: models.Member = Depends(get_current_active_member),
):
    article: models.Article = crud.get_article(db, article_id)
    if current_member.id != article.writer_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="no premission to set article's category",
        )

    success = crud.set_article_category(db, article_id, category)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="fail to set article category",
        )


@router.put("/{article_id}/tag", tags=["tag"])
async def add_article_tag(
    tag: schemas.TagWithName,
    article_id: int = Path(gt=0),
    db: Session = Depends(get_db),
    current_member: models.Member = Depends(get_current_active_member),
):
    article: models.Article = crud.get_article(db, article_id)
    if current_member.id != article.writer_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="no premission to add tag to article",
        )

    success = crud.add_article_tag(db, article_id, tag)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="fail to add article tag",
        )


@router.delete("/{article_id}/tag/{tag_id}", tags=["tag"])
async def remove_article_tag(
    article_id: int = Path(gt=0),
    tag_id: int = Path(gt=0),
    db: Session = Depends(get_db),
    current_member: models.Member = Depends(get_current_active_member),
):
    article: models.Article = crud.get_article(db, article_id)
    if current_member.id != article.writer_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="no premission to remove tags of article",
        )

    success = crud.remove_article_tag(db, article_id, tag_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="fail to remove article tag",
        )


@router.get(
    "/{article_id}/comment", response_model=list[schemas.Comment], tags=["comment"]
)
async def list_article_comments(
    response: Response,
    article_id: int = Path(gt=0),
    order_by: str = Query("-create_time", pattern="^-?(create_time|like|dislike)$"),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, gt=0),
    db: Session = Depends(get_db),
):
    comments, total = crud.list_comments(db, article_id, order_by, skip, limit)
    response.headers["X-Total-Count"] = str(total)
    return comments


@router.post("/{article_id}/comment", response_model=schemas.Comment, tags=["comment"])
async def create_article_comment(
    comment: schemas.CommentCreate,
    article_id: int = Path(gt=0),
    db: Session = Depends(get_db),
    current_member: models.Member = Depends(get_current_active_member),
):
    if comment.commenter_name is not None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="member should not set name",
        )
    result_comment = crud.create_comment(db, article_id, current_member.id, comment)
    if result_comment is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="fail to create comment"
        )
    return result_comment


@router.post(
    "/{article_id}/comment/visitor", response_model=schemas.Comment, tags=["comment"]
)
async def create_article_comment_for_visitor(
    comment: schemas.CommentCreate,
    article_id: int = Path(gt=0),
    db: Session = Depends(get_db),
):
    if comment.commenter_name is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="visitor must set name",
        )
    result_comment = crud.create_comment(db, article_id, None, comment)
    if result_comment is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="fail to create comment"
        )
    return result_comment

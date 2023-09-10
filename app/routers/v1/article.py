from datetime import datetime
from fastapi import APIRouter, Depends, Path, HTTPException, Query, status, Body

from sqlalchemy.orm import Session
from ... import crud, schemas
from ...dependencies.database import get_db

router = APIRouter(
    prefix="/article",
    tags=["article"],
)


@router.get("/", response_model=list[schemas.ArticleSimplify])
async def list_articles(
    title_like: str = Query(None, min_length=1, max_length=50),
    content_has: str = None,
    category_id: int = Query(None, gt=0),
    tag_ids: list[int] = Query(None),
    writer_ids: list[int] = Query(None),
    create_time_after: datetime = None,
    create_time_before: datetime = None,
    update_time_after: datetime = None,
    update_time_before: datetime = None,
    is_deleted: bool = None,
    order_by: str = Query(
        "-create_time", pattern="^-?(create_time|update_time|title)$"
    ),
    db: Session = Depends(get_db),
):
    articles = crud.list_articles(
        db,
        title_like,
        content_has,
        category_id,
        tag_ids,
        writer_ids,
        create_time_after,
        create_time_before,
        update_time_after,
        update_time_before,
        is_deleted,
        order_by,
    )
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
async def create_article(article: schemas.ArticleCreate, db: Session = Depends(get_db)):
    if crud.get_article_by_title(db, article.title) is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="article title already exist"
        )
    article_created = crud.create_article(db, article)
    if article_created is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="fail to create article"
        )
    return article_created


@router.delete("/{article_id}")
async def delete_article(article_id: int = Path(gt=0), db: Session = Depends(get_db)):
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
):
    success = crud.update_article(db, article_id, article)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="fail to update article"
        )

from fastapi import APIRouter, Depends, Path, HTTPException, status, Body

from sqlalchemy.orm import Session
from ... import crud, schemas
from ...dependencies.database import get_db
from ...dependencies.member import get_current_active_member

router = APIRouter(
    prefix="/category",
    tags=["category"],
)


@router.get("/", response_model=list[schemas.Category])
async def list_categories(hide_unused: bool = False, db: Session = Depends(get_db)):
    categorys = crud.list_categories(db, hide_unused)
    return categorys


@router.get("/{category_id}", response_model=schemas.Category)
async def get_category(category_id: int = Path(gt=0), db: Session = Depends(get_db)):
    result_category = crud.get_category(db, category_id)
    if result_category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="category not found"
        )
    return result_category


@router.post(
    "/",
    response_model=schemas.Category,
    dependencies=[Depends(get_current_active_member)],
)
async def create_category(
    category: schemas.CategoryCreate, db: Session = Depends(get_db)
):
    if crud.get_category_by_name(db, category.name) is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="category already exist"
        )

    category_created = crud.create_category(db, category)
    if category_created is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="fail to create category"
        )
    return category_created


@router.delete("/{category_id}", dependencies=[Depends(get_current_active_member)])
async def delete_category(category_id: int = Path(gt=0), db: Session = Depends(get_db)):
    success = crud.delete_category(db, category_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="fail to delete category"
        )

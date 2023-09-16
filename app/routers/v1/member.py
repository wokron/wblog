from fastapi import APIRouter, Depends, Query, Path, HTTPException, status

from sqlalchemy.orm import Session
from ... import crud, schemas, models
from ...dependencies.database import get_db
from ...dependencies.member import get_current_active_member

router = APIRouter(
    prefix="/member",
    tags=["member"],
)


@router.get(
    "/",
    response_model=list[schemas.Member],
    dependencies=[Depends(get_current_active_member)],
)
async def list_members(
    name_like: str = Query(None, min_length=1, max_length=20),
    role: models.Role = None,
    is_active: bool = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, gt=0),
    db: Session = Depends(get_db),
):
    members = crud.list_members(db, name_like, role, is_active, skip, limit)
    return members


@router.get("/me", response_model=schemas.Member)
async def get_current_member(
    current_member: models.Member = Depends(get_current_active_member),
):
    return current_member


@router.get(
    "/{member_id}",
    response_model=schemas.Member,
    dependencies=[Depends(get_current_active_member)],
)
async def get_member_by_id(member_id: int = Path(gt=0), db: Session = Depends(get_db)):
    result_member = crud.get_member(db, member_id)
    if result_member is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="member not found"
        )
    return result_member


@router.get(
    "/{member_name}",
    response_model=schemas.Member,
    dependencies=[Depends(get_current_active_member)],
)
async def get_member_by_name(
    member_name: str = Path(min_length=1, max_length=20), db: Session = Depends(get_db)
):
    result_member = crud.get_member_by_name(db, member_name)
    if result_member is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="member not found"
        )
    return result_member


@router.post("/", response_model=schemas.Member)
async def create_member(
    member: schemas.MemberCreate,
    db: Session = Depends(get_db),
    current_member: models.Member = Depends(get_current_active_member),
):
    if (
        member.role == models.Role.OWNER
        or current_member.role == models.Role.MEMBER
        or (
            member.role == models.Role.MANAGER
            and current_member.role == models.Role.MANAGER
        )
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="no premission to create member with that role",
        )
    if crud.get_member_by_name(db, member.name) is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="name already exist"
        )
    member_created = crud.create_member(db, member)
    if member_created is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="fail to create member"
        )
    return member_created


@router.patch("/{member_id}")
async def update_member(
    member: schemas.MemberUpdate,
    member_id: int = Path(gt=0),
    db: Session = Depends(get_db),
    current_member: models.Member = Depends(get_current_active_member),
):
    if (
        current_member.id != member_id
        and (
            member.role == models.Role.OWNER
            or current_member.role == models.Role.MEMBER
            or (
                member.role == models.Role.MANAGER
                and current_member.role == models.Role.MANAGER
            )
        )
    ) or (current_member.id == member_id and member.role is not None):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="no premission to update member info",
        )
    success = crud.update_member(db, member_id, member)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="fail to update member"
        )

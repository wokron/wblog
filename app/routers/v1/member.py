from fastapi import APIRouter

router = APIRouter(
    prefix="/member",
    tags=["member"],
)


@router.get("/")
async def test():
    return {"msg": "hello"}

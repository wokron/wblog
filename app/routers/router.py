from fastapi import APIRouter
from .v1 import member

apiv1 = APIRouter(
    prefix="/api/v1",
    tags=["v1"],
)

apiv1.include_router(member.router)

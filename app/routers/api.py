from fastapi import APIRouter
from .v1 import v1
from . import token

router = APIRouter(
    prefix="/api",
)

router.include_router(v1.router)

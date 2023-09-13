from fastapi import APIRouter
from .v1 import v1
from . import token

api = APIRouter(
    prefix="/api",
)

api.include_router(v1.router)

from fastapi import APIRouter
from . import api, token

router = APIRouter()

router.include_router(api.router)
router.include_router(token.router)

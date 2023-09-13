from fastapi import APIRouter
from . import member, category, tag, article, comment


router = APIRouter(
    prefix="/v1",
    tags=["v1"],
)

router.include_router(member.router)
router.include_router(category.router)
router.include_router(tag.router)
router.include_router(article.router)
router.include_router(comment.router)

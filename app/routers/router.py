from fastapi import APIRouter
from .v1 import member, category, tag, article, comment

apiv1 = APIRouter(
    prefix="/api/v1",
    tags=["v1"],
)

apiv1.include_router(member.router)
apiv1.include_router(category.router)
apiv1.include_router(tag.router)
apiv1.include_router(article.router)
apiv1.include_router(comment.router)

from fastapi import FastAPI

from .routers import router, token
from .core import database

database.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

app.include_router(router.api)
app.include_router(token.auth)

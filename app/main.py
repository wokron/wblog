from fastapi import FastAPI

from .routers import router
from .core import database

database.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

app.include_router(router.apiv1)

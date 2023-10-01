from fastapi import FastAPI

from .routers import router
from . import database

database.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

app.include_router(router)

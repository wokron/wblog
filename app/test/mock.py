from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from ..core.database import Base
from ..main import app
from ..dependencies.database import get_db
from ..dependencies.config import get_settings
from ..config import Settings


engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def get_db_override():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


def get_settings_override():
    return Settings(secret_key="secret_key_for_test")


app.dependency_overrides[get_db] = get_db_override
app.dependency_overrides[get_settings] = get_settings_override

client = TestClient(app)

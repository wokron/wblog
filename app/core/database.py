from sqlalchemy import create_engine, URL
from sqlalchemy.orm import sessionmaker, declarative_base
from ..dependencies import config


settings = config.get_settings()

if settings.db_url is not None:
    connect_url = settings.db_url
else:
    connect_url = URL.create(
        drivername=settings.db_drivername,
        username=settings.db_username,
        password=settings.db_password,
        host=settings.db_host,
        port=settings.db_port,
        database=settings.db_database,
        query=settings.db_query.model_dump(),
    )

engine = create_engine(connect_url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

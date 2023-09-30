from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class DBQuerySettings(BaseSettings):
    model_config = SettingsConfigDict(extra="allow")


class Settings(BaseSettings):
    secret_key: str = Field(min_length=1)
    algorithm: str = "HS256"
    access_token_expire_minutes: int = Field(30, ge=1)

    owner_name: str = Field("Owner", min_length=1, max_length=20)
    owner_password: str = Field(
        "12345678", min_length=8, max_length=24, pattern="^[0-9a-zA-Z]+$"
    )

    db_url: str | None = None
    db_drivername: str = "sqlite"
    db_username: str | None = Field(None, min_length=1)
    db_password: str | None = Field(None, min_length=1)
    db_host: str | None = Field(None, min_length=1)
    db_port: int | None = Field(None, ge=0, le=65535)
    db_database: str = Field("wblog.db", min_length=1)
    db_query: DBQuerySettings = DBQuerySettings(check_same_thread="true")

    model_config = SettingsConfigDict(env_file=".env", env_nested_delimiter="__")

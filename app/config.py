from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    secret_key: str = Field(min_length=1)
    algorithm: str = "HS256"
    access_token_expire_minutes: int = Field(30, ge=1)
    owner_name: str = Field("Owner", min_length=1, max_length=20)
    owner_password: str = Field("12345678", min_length=8, max_length=24, pattern="^[0-9a-zA-Z]+$")

    model_config = SettingsConfigDict(env_file=".env")

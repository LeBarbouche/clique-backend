from functools import lru_cache

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Clique de Doissin API"
    app_env: str = "development"
    database_url: str = (
        "postgresql+psycopg://postgres:postgres@localhost:5432/clique_doissin"
    )
    cors_origins: list[str] = ["http://localhost:5173"]
    auth_secret: str
    auth_token_expire_minutes: int = 60 * 24

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @field_validator("cors_origins", mode="before")
    @classmethod
    def split_origins(cls, value: object) -> object:
        if isinstance(value, str):
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        return value

    @field_validator("auth_secret")
    @classmethod
    def validate_auth_secret(cls, value: str) -> str:
        if len(value) < 32:
            raise ValueError("AUTH_SECRET doit contenir au moins 32 caractères")
        return value


@lru_cache
def get_settings() -> Settings:
    return Settings()

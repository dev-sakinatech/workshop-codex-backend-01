from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = Field(default="RBAC API", description="Application name")
    database_url: str = Field(
        default="postgresql+psycopg2://postgres:postgres@localhost:5432/rbac",
        description="SQLAlchemy-compatible database URL",
    )
    debug: bool = Field(default=True)

    class Config:
        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    return Settings()

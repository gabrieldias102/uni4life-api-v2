import os
from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "uni4life API"
    app_version: str = "0.1.0"
    api_prefix: str = ""
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./db.sqlite3")

    db_echo: bool = False
    cors_allow_origins: str = ""
    cors_allow_credentials: bool = True

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


    @property
    def cors_origins_list(self) -> list[str]:
        if not self.cors_allow_origins:
            return []

        return [origin.strip() for origin in self.cors_allow_origins.split(",") if origin.strip()]


@lru_cache()
def get_settings() -> Settings:
    return Settings()
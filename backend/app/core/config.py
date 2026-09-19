from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    environment: str = "local"

    database_url: str
    redis_url: str
    celery_broker_url: str

    secret_key: str

    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 30

    frontend_url: str = "http://localhost:5173"
    allowed_origins: str = "http://localhost:5173"

    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env.local",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def cors_origins(self) -> list[str]:
        return [
            origin.strip()
            for origin in self.allowed_origins.split(",")
            if origin.strip()
        ]


@lru_cache
def get_settings() -> Settings:
    return Settings()
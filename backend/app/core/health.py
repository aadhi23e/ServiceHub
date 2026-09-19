from dataclasses import dataclass

import redis
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.core.config import get_settings
from app.db.session import engine


@dataclass(frozen=True)
class DependencyHealth:
    postgres: bool
    redis: bool

    @property
    def is_ready(self) -> bool:
        return self.postgres and self.redis


def check_postgres() -> bool:
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return True
    except SQLAlchemyError:
        return False


def check_redis() -> bool:
    settings = get_settings()

    try:
        client = redis.from_url(
            settings.redis_url,
            socket_connect_timeout=2,
            socket_timeout=2,
        )

        try:
            return bool(client.ping())
        finally:
            client.close()

    except redis.RedisError:
        return False


def check_dependencies() -> DependencyHealth:
    return DependencyHealth(
        postgres=check_postgres(),
        redis=check_redis(),
    )
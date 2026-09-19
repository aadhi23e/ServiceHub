from redis import Redis

from app.db.redis import redis_client


def get_redis() -> Redis:
    return redis_client
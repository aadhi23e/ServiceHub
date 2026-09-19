import redis

from app.core.config import get_settings
from app.core.rate_limit import RateLimiter


def test_rate_limiter_uses_atomic_redis_script():
    settings = get_settings()

    redis_client = redis.Redis.from_url(
        settings.redis_url,
        decode_responses=True,
    )

    key = "servicehub:test:rate_limit:atomic"

    try:
        redis_client.delete(key)

        limiter = RateLimiter(redis_client)

        first = limiter.check(
            key=key,
            limit=2,
            window_seconds=60,
            policy="general"
        )

        second = limiter.check(
            key=key,
            limit=2,
            window_seconds=60,
            policy="general"
        )

        third = limiter.check(
            key=key,
            limit=2,
            window_seconds=60,
            policy="general"
        )

        assert first.allowed is True
        assert first.remaining == 1

        assert second.allowed is True
        assert second.remaining == 0

        assert third.allowed is False
        assert third.remaining == 0

        ttl = redis_client.ttl(key)

        assert 0 < ttl <= 60

    finally:
        redis_client.delete(key)
        redis_client.close()


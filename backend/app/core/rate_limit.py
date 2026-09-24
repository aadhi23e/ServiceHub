from dataclasses import dataclass

import redis
import structlog
from redis import Redis

from app.core.exceptions import RateLimitError

logger = structlog.get_logger()


RATE_LIMIT_SCRIPT = """
local current = redis.call("INCR", KEYS[1])

if current == 1 then
    redis.call("EXPIRE", KEYS[1], ARGV[1])
end

local ttl = redis.call("TTL", KEYS[1])

return {current, ttl}
"""


@dataclass(frozen=True)
class RateLimitResult:
    allowed: bool
    limit: int
    remaining: int
    retry_after: int
    policy: str


def build_rate_limit_key(
    *,
    identifier: str,
    policy: str,
) -> str:
    return f"servicehub:rate_limit:ip:{identifier}:{policy}"


class RateLimiter:
    def __init__(self, redis_client: Redis) -> None:
        self.redis = redis_client

    def check(
        self,
        *,
        key: str,
        limit: int,
        window_seconds: int,
        policy: str,
    ) -> RateLimitResult:
        if limit <= 0:
            raise ValueError("limit must be greater than zero")

        if window_seconds <= 0:
            raise ValueError("window_seconds must be greater than zero")

        if not policy:
            raise ValueError("policy must not be empty")

        try:
            result = self.redis.eval(
                RATE_LIMIT_SCRIPT,
                1,
                key,
                window_seconds,
            )

            current = int(result[0])
            ttl = max(int(result[1]), 1)

            allowed = current <= limit
            remaining = max(limit - current, 0)

            return RateLimitResult(
                allowed=allowed,
                limit=limit,
                remaining=remaining,
                retry_after=ttl,
                policy=policy,
            )

        except redis.RedisError:
            logger.exception(
                "rate_limit_redis_error",
                rate_limit_key=key,
                rate_limit_policy=policy,
            )

            return RateLimitResult(
                allowed=True,
                limit=limit,
                remaining=limit,
                retry_after=0,
                policy=policy,
            )

    def enforce(
        self,
        *,
        key: str,
        limit: int,
        window_seconds: int,
        policy: str,
    ) -> RateLimitResult:
        result = self.check(
            key=key,
            limit=limit,
            window_seconds=window_seconds,
            policy=policy,
        )

        if not result.allowed:
            raise RateLimitError(
                retry_after=result.retry_after,
                limit=result.limit,
                remaining=result.remaining,
                policy=result.policy,
            )

        return result

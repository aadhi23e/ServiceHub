from collections.abc import Callable

from fastapi import Depends, Request
from redis import Redis

from app.core.config import get_settings
from app.core.dependencies import get_redis
from app.core.rate_limit import RateLimiter, build_rate_limit_key
from app.core.rate_limit_policy import RateLimitPolicy
from app.core.rate_limit_policy import (
    get_general_rate_limit_policy,
    get_login_rate_limit_policy,
    get_refresh_rate_limit_policy,
    get_registration_rate_limit_policy,
)


def create_rate_limit_dependency(
    policy_factory: Callable[[], RateLimitPolicy],
):
    def rate_limit_dependency(
        request: Request,
        redis_client: Redis = Depends(get_redis),
    ) -> None:
        settings = get_settings()

        if not settings.rate_limit_enabled:
            return

        policy = policy_factory()

        identifier = (
            request.client.host
            if request.client
            else "unknown"
        )

        key = build_rate_limit_key(
            identifier=identifier,
            policy=policy.name,
        )

        limiter = RateLimiter(redis_client)

        limiter.enforce(
            key=key,
            limit=policy.requests,
            window_seconds=policy.window_seconds,
            policy=policy.name,
        )

    return rate_limit_dependency


general_rate_limit = create_rate_limit_dependency(
    get_general_rate_limit_policy,
)

registration_rate_limit = create_rate_limit_dependency(
    get_registration_rate_limit_policy,
)

login_rate_limit = create_rate_limit_dependency(
    get_login_rate_limit_policy,
)

refresh_rate_limit = create_rate_limit_dependency(
    get_refresh_rate_limit_policy,
)
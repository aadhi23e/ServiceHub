from unittest.mock import Mock, patch

from fastapi import Request

from app.core.rate_limit_dependencies import (
    create_rate_limit_dependency,
)
from app.core.rate_limit_policy import RateLimitPolicy


def make_request(
    host: str = "203.0.113.10",
) -> Request:
    scope = {
        "type": "http",
        "method": "GET",
        "path": "/test",
        "headers": [],
        "client": (host, 12345),
        "scheme": "http",
        "server": ("testserver", 80),
    }

    return Request(scope)


def test_rate_limit_dependency_uses_client_ip():
    policy = RateLimitPolicy(
        name="test",
        requests=10,
        window_seconds=60,
    )

    redis_client = Mock()

    with patch("app.core.rate_limit_dependencies.RateLimiter") as limiter_class:
        limiter = limiter_class.return_value

        dependency = create_rate_limit_dependency(
            lambda: policy,
        )

        dependency(
            request=make_request("203.0.113.25"),
            redis_client=redis_client,
        )

        limiter_class.assert_called_once_with(redis_client)

        limiter.enforce.assert_called_once_with(
            key="servicehub:rate_limit:ip:203.0.113.25:test",
            limit=10,
            window_seconds=60,
            policy="test",
        )


def test_rate_limit_dependency_uses_unknown_when_client_missing():
    policy = RateLimitPolicy(
        name="test",
        requests=10,
        window_seconds=60,
    )

    redis_client = Mock()

    request = Request(
        {
            "type": "http",
            "method": "GET",
            "path": "/test",
            "headers": [],
            "client": None,
            "scheme": "http",
            "server": ("testserver", 80),
        }
    )

    with patch("app.core.rate_limit_dependencies.RateLimiter") as limiter_class:
        limiter = limiter_class.return_value

        dependency = create_rate_limit_dependency(
            lambda: policy,
        )

        dependency(
            request=request,
            redis_client=redis_client,
        )

        limiter.enforce.assert_called_once_with(
            key="servicehub:rate_limit:ip:unknown:test",
            limit=10,
            window_seconds=60,
            policy="test",
        )


def test_rate_limit_dependency_does_nothing_when_disabled():
    policy = RateLimitPolicy(
        name="test",
        requests=10,
        window_seconds=60,
    )

    redis_client = Mock()

    with patch("app.core.rate_limit_dependencies.get_settings") as get_settings:
        get_settings.return_value.rate_limit_enabled = False

        with patch("app.core.rate_limit_dependencies.RateLimiter") as limiter_class:
            dependency = create_rate_limit_dependency(
                lambda: policy,
            )

            dependency(
                request=make_request(),
                redis_client=redis_client,
            )

            limiter_class.assert_not_called()

from unittest.mock import Mock

import redis
import pytest

from app.core.rate_limit import (
    RateLimiter,
    build_rate_limit_key,
)
from app.core.exceptions import RateLimitError

def test_build_rate_limit_key():
    key = build_rate_limit_key(
        identifier="203.0.113.10",
        policy="general",
    )

    assert key == (
        "servicehub:rate_limit:ip:203.0.113.10:general"
    )


def test_rate_limiter_allows_request_under_limit():
    redis_client = Mock()
    redis_client.eval.return_value = [1, 60]

    limiter = RateLimiter(redis_client)

    result = limiter.check(
        key="servicehub:rate_limit:ip:203.0.113.10:general",
        limit=100,
        window_seconds=60,
        policy="general",
    )

    assert result.allowed is True
    assert result.limit == 100
    assert result.remaining == 99
    assert result.retry_after == 60
    assert result.policy == "general"

    redis_client.eval.assert_called_once()


def test_rate_limiter_rejects_request_over_limit():
    redis_client = Mock()
    redis_client.eval.return_value = [101, 42]

    limiter = RateLimiter(redis_client)

    result = limiter.check(
        key="servicehub:rate_limit:ip:203.0.113.10:general",
        limit=100,
        window_seconds=60,
policy="general",

    )

    assert result.allowed is False
    assert result.limit == 100
    assert result.remaining == 0
    assert result.retry_after == 42


def test_rate_limiter_allows_last_request():
    redis_client = Mock()
    redis_client.eval.return_value = [100, 12]

    limiter = RateLimiter(redis_client)

    result = limiter.check(
        key="servicehub:rate_limit:ip:203.0.113.10:general",
        limit=100,
        window_seconds=60,
policy="general",

    )

    assert result.allowed is True
    assert result.remaining == 0
    assert result.retry_after == 12


def test_rate_limiter_never_returns_negative_remaining():
    redis_client = Mock()
    redis_client.eval.return_value = [150, 20]

    limiter = RateLimiter(redis_client)

    result = limiter.check(
        key="servicehub:rate_limit:ip:203.0.113.10:general",
        limit=100,
        window_seconds=60,
policy="general",

    )

    assert result.allowed is False
    assert result.remaining == 0


def test_rate_limiter_clamps_invalid_ttl():
    redis_client = Mock()
    redis_client.eval.return_value = [1, -1]

    limiter = RateLimiter(redis_client)

    result = limiter.check(
        key="servicehub:rate_limit:ip:203.0.113.10:general",
        limit=100,
        window_seconds=60,
policy="general",

    )

    assert result.retry_after == 1


def test_rate_limiter_fails_open_when_redis_fails():
    redis_client = Mock()
    redis_client.eval.side_effect = redis.RedisError(
        "Redis unavailable"
    )

    limiter = RateLimiter(redis_client)

    result = limiter.check(
        key="servicehub:rate_limit:ip:203.0.113.10:general",
        limit=100,
        window_seconds=60,
        policy="general",
    )

    assert result.allowed is True
    assert result.limit == 100
    assert result.remaining == 100
    assert result.retry_after == 0
    assert result.policy == "general"


def test_rate_limiter_rejects_invalid_limit():
    redis_client = Mock()

    limiter = RateLimiter(redis_client)

    with pytest.raises(ValueError, match="limit must be greater than zero"):
        limiter.check(
            key="servicehub:rate_limit:ip:203.0.113.10:general",
            limit=0,
            window_seconds=60,
policy="general",

        )

    redis_client.eval.assert_not_called()


def test_rate_limiter_rejects_invalid_window():
    redis_client = Mock()

    limiter = RateLimiter(redis_client)

    with pytest.raises(
        ValueError,
        match="window_seconds must be greater than zero",
    ):
        limiter.check(
            key="servicehub:rate_limit:ip:203.0.113.10:general",
            limit=100,
            window_seconds=0,
            policy="general",
        )

    redis_client.eval.assert_not_called()

def test_rate_limiter_enforce_allows_request():
    redis_client = Mock()
    redis_client.eval.return_value = [1, 60]

    limiter = RateLimiter(redis_client)

    result = limiter.enforce(
        key="servicehub:rate_limit:ip:203.0.113.10:general",
        limit=100,
        window_seconds=60,
policy="general",

    )

    assert result.allowed is True
    assert result.remaining == 99


def test_rate_limiter_enforce_raises_rate_limit_error():
    redis_client = Mock()
    redis_client.eval.return_value = [101, 37]

    limiter = RateLimiter(redis_client)

    with pytest.raises(RateLimitError) as exc_info:
        limiter.enforce(
            key="servicehub:rate_limit:ip:203.0.113.10:general",
            limit=100,
            window_seconds=60,
policy="general",

        )

    assert exc_info.value.status_code == 429
    assert exc_info.value.code == "RATE_LIMITED"
    assert exc_info.value.retry_after == 37

def test_rate_limiter_rejects_empty_policy():
    redis_client = Mock()

    limiter = RateLimiter(redis_client)

    with pytest.raises(
        ValueError,
        match="policy must not be empty",
    ):
        limiter.check(
            key="servicehub:rate_limit:ip:203.0.113.10:general",
            limit=100,
            window_seconds=60,
            policy="",
        )

    redis_client.eval.assert_not_called()

def test_rate_limiter_enforce_preserves_rate_limit_metadata():
    redis_client = Mock()
    redis_client.eval.return_value = [101, 37]

    limiter = RateLimiter(redis_client)

    with pytest.raises(RateLimitError) as exc_info:
        limiter.enforce(
            key="servicehub:rate_limit:ip:203.0.113.10:general",
            limit=100,
            window_seconds=60,
            policy="general",
        )

    error = exc_info.value

    assert error.retry_after == 37
    assert error.limit == 100
    assert error.remaining == 0
    assert error.policy == "general"
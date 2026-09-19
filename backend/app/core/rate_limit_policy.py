from dataclasses import dataclass

from app.core.config import get_settings


@dataclass(frozen=True)
class RateLimitPolicy:
    name: str
    requests: int
    window_seconds: int


def get_general_rate_limit_policy() -> RateLimitPolicy:
    settings = get_settings()

    return RateLimitPolicy(
        name="general",
        requests=settings.rate_limit_general_requests_per_minute,
        window_seconds=settings.rate_limit_window_seconds,
    )


def get_registration_rate_limit_policy() -> RateLimitPolicy:
    settings = get_settings()

    return RateLimitPolicy(
        name="registration",
        requests=settings.rate_limit_registration_requests_per_minute,
        window_seconds=settings.rate_limit_window_seconds,
    )


def get_login_rate_limit_policy() -> RateLimitPolicy:
    settings = get_settings()

    return RateLimitPolicy(
        name="login",
        requests=settings.rate_limit_login_requests_per_minute,
        window_seconds=settings.rate_limit_window_seconds,
    )


def get_refresh_rate_limit_policy() -> RateLimitPolicy:
    settings = get_settings()

    return RateLimitPolicy(
        name="refresh",
        requests=settings.rate_limit_refresh_requests_per_minute,
        window_seconds=settings.rate_limit_window_seconds,
    )
from app.core.rate_limit_policy import (
    get_general_rate_limit_policy,
    get_login_rate_limit_policy,
    get_refresh_rate_limit_policy,
    get_registration_rate_limit_policy,
)


def test_general_policy():
    policy = get_general_rate_limit_policy()

    assert policy.name == "general"
    assert policy.requests == 100
    assert policy.window_seconds == 60


def test_registration_policy():
    policy = get_registration_rate_limit_policy()

    assert policy.name == "registration"
    assert policy.requests == 5
    assert policy.window_seconds == 60


def test_login_policy():
    policy = get_login_rate_limit_policy()

    assert policy.name == "login"
    assert policy.requests == 5
    assert policy.window_seconds == 60


def test_refresh_policy():
    policy = get_refresh_rate_limit_policy()

    assert policy.name == "refresh"
    assert policy.requests == 10
    assert policy.window_seconds == 60
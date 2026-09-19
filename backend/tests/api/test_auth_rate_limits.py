from app.api.v1.auth import router
from app.core.rate_limit_dependencies import (
    login_rate_limit,
    refresh_rate_limit,
    registration_rate_limit,
)


def test_auth_router_contains_registration_rate_limit():
    route = next(
        route
        for route in router.routes
        if route.path.endswith("/register")
    )

    dependency_functions = {
        dependency.call
        for dependency in route.dependencies
    }

    assert registration_rate_limit in dependency_functions


def test_auth_router_contains_login_rate_limit():
    route = next(
        route
        for route in router.routes
        if route.path.endswith("/login")
    )

    dependency_functions = {
        dependency.call
        for dependency in route.dependencies
    }

    assert login_rate_limit in dependency_functions


def test_auth_router_contains_refresh_rate_limit():
    route = next(
        route
        for route in router.routes
        if route.path.endswith("/refresh")
    )

    dependency_functions = {
        dependency.call
        for dependency in route.dependencies
    }

    assert refresh_rate_limit in dependency_functions
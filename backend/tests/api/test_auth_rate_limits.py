from fastapi import Depends

from app.api.v1.auth import router
from app.core.rate_limit_dependencies import (
    login_rate_limit,
    refresh_rate_limit,
    registration_rate_limit,
)


def get_route(path_suffix: str):
    return next(
        route
        for route in router.routes
        if route.path.endswith(path_suffix)
    )


def get_dependency_functions(route):
    return {
        dependency.dependency
        for dependency in route.dependencies
        if isinstance(dependency, Depends)
    }


def test_auth_router_contains_registration_rate_limit():
    route = get_route("/register")

    dependency_functions = get_dependency_functions(route)

    assert registration_rate_limit in dependency_functions


def test_auth_router_contains_login_rate_limit():
    route = get_route("/login")

    dependency_functions = get_dependency_functions(route)

    assert login_rate_limit in dependency_functions


def test_auth_router_contains_refresh_rate_limit():
    route = get_route("/refresh")

    dependency_functions = get_dependency_functions(route)

    assert refresh_rate_limit in dependency_functions
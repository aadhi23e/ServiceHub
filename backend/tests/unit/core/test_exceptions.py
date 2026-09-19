from app.core.exceptions import (
    AuthenticationError,
    AuthorizationError,
    ConflictError,
    DependencyUnavailableError,
    RateLimitError,
    ResourceNotFoundError,
    ServiceHubError,
    ValidationError,
)


def test_base_servicehub_error_defaults():
    error = ServiceHubError()

    assert error.status_code == 400
    assert error.code == "SERVICE_ERROR"
    assert error.message == "An application error occurred."


def test_authentication_error_defaults():
    error = AuthenticationError()

    assert error.status_code == 401
    assert error.code == "AUTHENTICATION_FAILED"


def test_authorization_error_defaults():
    error = AuthorizationError()

    assert error.status_code == 403
    assert error.code == "FORBIDDEN"


def test_not_found_error_defaults():
    error = ResourceNotFoundError()

    assert error.status_code == 404
    assert error.code == "RESOURCE_NOT_FOUND"


def test_conflict_error_defaults():
    error = ConflictError()

    assert error.status_code == 409
    assert error.code == "CONFLICT"


def test_validation_error_defaults():
    error = ValidationError()

    assert error.status_code == 422
    assert error.code == "VALIDATION_ERROR"


def test_rate_limit_error_defaults():
    error = RateLimitError()

    assert error.status_code == 429
    assert error.code == "RATE_LIMITED"


def test_dependency_error_defaults():
    error = DependencyUnavailableError()

    assert error.status_code == 503
    assert error.code == "DEPENDENCY_UNAVAILABLE"


def test_custom_servicehub_error():
    error = ConflictError(
        message="The booking conflicts with another booking.",
        code="BOOKING_SLOT_UNAVAILABLE",
    )

    assert error.status_code == 409
    assert error.code == "BOOKING_SLOT_UNAVAILABLE"
    assert error.message == "The booking conflicts with another booking."

def test_rate_limit_error_supports_retry_after():
    error = RateLimitError(
        retry_after=37,
    )

    assert error.status_code == 429
    assert error.code == "RATE_LIMITED"
    assert error.message == "Too many requests. Please try again later."
    assert error.retry_after == 37


def test_rate_limit_error_clamps_negative_retry_after():
    error = RateLimitError(
        retry_after=-10,
    )

    assert error.retry_after == 0

def test_rate_limit_error_supports_rate_limit_metadata():
    error = RateLimitError(
        retry_after=37,
        limit=100,
        remaining=0,
        policy="general",
    )

    assert error.status_code == 429
    assert error.code == "RATE_LIMITED"
    assert error.message == (
        "Too many requests. Please try again later."
    )

    assert error.retry_after == 37
    assert error.limit == 100
    assert error.remaining == 0
    assert error.policy == "general"

def test_rate_limit_error_clamps_metadata():
    error = RateLimitError(
        retry_after=-10,
        limit=-100,
        remaining=-5,
        policy="general",
    )

    assert error.retry_after == 0
    assert error.limit == 0
    assert error.remaining == 0
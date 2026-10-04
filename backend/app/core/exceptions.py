from typing import Any


class ServiceHubError(Exception):
    """Base exception for expected ServiceHub application errors."""

    status_code = 400
    code = "SERVICE_ERROR"
    message = "An application error occurred."

    def __init__(
        self,
        message: str | None = None,
        *,
        code: str | None = None,
        status_code: int | None = None,
        details: Any | None = None,
    ) -> None:
        super().__init__(message or self.message)

        self.message = message or self.message
        self.code = code or self.code
        self.status_code = status_code or self.status_code
        self.details = details


class AuthenticationError(ServiceHubError):
    """Raised when authentication fails."""

    status_code = 401
    code = "AUTHENTICATION_FAILED"
    message = "Authentication failed."


class AuthorizationError(ServiceHubError):
    """Raised when an authenticated user lacks permission."""

    status_code = 403
    code = "FORBIDDEN"
    message = "You do not have permission to perform this action."


class ResourceNotFoundError(ServiceHubError):
    """Raised when a requested resource does not exist."""

    status_code = 404
    code = "RESOURCE_NOT_FOUND"
    message = "The requested resource was not found."


class ConflictError(ServiceHubError):
    """Raised when an operation conflicts with current state."""

    status_code = 409
    code = "CONFLICT"
    message = "The requested operation conflicts with the current state."

class ResourceConflictError(ServiceHubError):
    """Raised when an operation conflicts with current state."""

    status_code = 409
    code = "RESOURCE_CONFLICT"
    message = "The requested resource is already exicts"


class ValidationError(ServiceHubError):
    """Raised when application-level validation fails."""

    status_code = 422
    code = "VALIDATION_ERROR"
    message = "The provided data is invalid."


class RateLimitError(ServiceHubError):
    """Raised when a client exceeds a rate limit."""

    status_code = 429
    code = "RATE_LIMITED"
    message = "Too many requests. Please try again later."

    def __init__(
        self,
        message: str | None = None,
        *,
        retry_after: int = 0,
        limit: int = 0,
        remaining: int = 0,
        policy: str = "",
        details: object | None = None,
    ) -> None:
        super().__init__(
            message=message,
            details=details,
        )

        self.retry_after = max(retry_after, 0)
        self.limit = max(limit, 0)
        self.remaining = max(remaining, 0)
        self.policy = policy


class DependencyUnavailableError(ServiceHubError):
    """Raised when a required dependency is unavailable."""

    status_code = 503
    code = "DEPENDENCY_UNAVAILABLE"
    message = "A required service is temporarily unavailable."


# class ResourceConflictError(Exception):
#     def __init__(self, message: str):
#         self.message = message
#         super().__init__(message)


# TODO: remove the below ones they are for references only
"""
raise ResourceNotFoundError(
    message="Provider not found.",
    code="PROVIDER_NOT_FOUND",
)

or

raise ConflictError(
    message="The selected time is no longer available.",
    code="BOOKING_SLOT_UNAVAILABLE",
)
"""

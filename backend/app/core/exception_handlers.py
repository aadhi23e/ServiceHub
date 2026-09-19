import structlog
from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.exceptions import ServiceHubError


logger = structlog.get_logger()


def _get_request_id(request: Request) -> str:
    request_id = getattr(request.state, "request_id", None)

    if request_id:
        return request_id

    return "req_unknown"


def _error_response(
    request: Request,
    *,
    status_code: int,
    code: str,
    message: str,
    details: object | None = None,
) -> JSONResponse:
    request_id = _get_request_id(request)

    error: dict[str, object] = {
        "code": code,
        "message": message,
        "request_id": request_id,
    }

    if details is not None:
        error["details"] = details

    return JSONResponse(
        status_code=status_code,
        content={
            "error": error,
        },
    )


async def servicehub_exception_handler(
    request: Request,
    exc: ServiceHubError,
) -> JSONResponse:
    logger.warning(
        "service_error",
        error_code=exc.code,
        status_code=exc.status_code,
    )

    return _error_response(
        request,
        status_code=exc.status_code,
        code=exc.code,
        message=exc.message,
        details=exc.details,
    )


async def http_exception_handler(
    request: Request,
    exc: StarletteHTTPException,
) -> JSONResponse:
    status_code = exc.status_code

    code_by_status = {
        400: "BAD_REQUEST",
        401: "UNAUTHENTICATED",
        403: "FORBIDDEN",
        404: "NOT_FOUND",
        405: "METHOD_NOT_ALLOWED",
        409: "CONFLICT",
        429: "RATE_LIMITED",
    }

    code = code_by_status.get(
        status_code,
        "HTTP_ERROR",
    )

    message = (
        exc.detail
        if isinstance(exc.detail, str)
        else "The request could not be completed."
    )

    logger.warning(
        "http_error",
        error_code=code,
        status_code=status_code,
    )

    return _error_response(
        request,
        status_code=status_code,
        code=code,
        message=message,
    )


async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    details = [
        {
            "location": error.get("loc", []),
            "message": error.get("msg", "Invalid value."),
            "type": error.get("type", "validation_error"),
        }
        for error in exc.errors()
    ]

    logger.warning(
        "request_validation_error",
        status_code=422,
    )

    return _error_response(
        request,
        status_code=422,
        code="VALIDATION_ERROR",
        message="The provided data is invalid.",
        details=details,
    )


async def unhandled_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    logger.exception(
        "unhandled_exception",
        exc_info=exc,
    )

    return _error_response(
        request,
        status_code=500,
        code="INTERNAL_SERVER_ERROR",
        message="An unexpected error occurred.",
    )
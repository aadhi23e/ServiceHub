from fastapi import APIRouter
from fastapi.testclient import TestClient

from app.main import app
from app.core.exceptions import (
    ConflictError,
    RateLimitError,
)

router = APIRouter(
    prefix="/test-errors",
)


@router.get("/servicehub-error")
def servicehub_error():
    raise ConflictError(
        message="This resource already exists.",
        code="RESOURCE_ALREADY_EXISTS",
    )


@router.get("/unexpected-error")
def unexpected_error():
    raise RuntimeError("This should never be exposed to the client.")

@router.get("/rate-limited")
def rate_limited_error():
    raise RateLimitError(
        retry_after=37,
    )

app.include_router(router)


client = TestClient(
    app,
    raise_server_exceptions=False,
)


def test_servicehub_error_response():
    response = client.get("/test-errors/servicehub-error")

    assert response.status_code == 409

    body = response.json()

    assert body["error"]["code"] == "RESOURCE_ALREADY_EXISTS"
    assert body["error"]["message"] == "This resource already exists."
    assert body["error"]["request_id"].startswith("req_")


def test_servicehub_error_request_id_propagation():
    request_id = "req_test_123"

    response = client.get(
        "/test-errors/servicehub-error",
        headers={"X-Request-ID": request_id},
    )

    assert response.status_code == 409
    assert response.headers["X-Request-ID"] == request_id

    body = response.json()

    assert body["error"]["request_id"] == request_id


def test_not_found_error_response():
    response = client.get("/this-route-does-not-exist")

    assert response.status_code == 404

    body = response.json()

    assert body["error"]["code"] == "NOT_FOUND"
    assert body["error"]["request_id"].startswith("req_")


def test_unhandled_error_response():
    response = client.get("/test-errors/unexpected-error")

    assert response.status_code == 500

    body = response.json()

    assert body["error"]["code"] == "INTERNAL_SERVER_ERROR"
    assert body["error"]["message"] == "An unexpected error occurred."
    assert body["error"]["request_id"].startswith("req_")

    assert "This should never be exposed" not in response.text

def test_rate_limit_error_response():
    response = client.get("/test-errors/rate-limited")

    assert response.status_code == 429

    body = response.json()

    assert body["error"]["code"] == "RATE_LIMITED"
    assert (
        body["error"]["message"]
        == "Too many requests. Please try again later."
    )

    assert body["error"]["request_id"].startswith("req_")

    assert response.headers["Retry-After"] == "37"

    assert response.headers["X-Request-ID"].startswith("req_")

def test_rate_limit_error_preserves_request_id():
    request_id = "req_rate_limit_test_123"

    response = client.get(
        "/test-errors/rate-limited",
        headers={
            "X-Request-ID": request_id,
        },
    )

    assert response.status_code == 429

    body = response.json()

    assert body["error"]["request_id"] == request_id
    assert response.headers["X-Request-ID"] == request_id
    assert response.headers["Retry-After"] == "37"
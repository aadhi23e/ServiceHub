from unittest.mock import Mock, patch

from app.core.security import hash_refresh_token
from app.services.auth_service import AuthService


def test_logout_hashes_and_revokes_refresh_token():
    db = Mock()
    redis_client = Mock()

    auth_service = AuthService(
        db=db,
        redis_client=redis_client,
    )

    refresh_token = "test-refresh-token"

    with patch.object(
        auth_service.auth_session_repository,
        "revoke",
    ) as revoke:
        auth_service.logout(refresh_token)

        expected_hash = hash_refresh_token(
            refresh_token,
        )

        revoke.assert_called_once_with(
            expected_hash,
        )


def test_logout_with_no_refresh_token_does_nothing():
    db = Mock()
    redis_client = Mock()

    auth_service = AuthService(
        db=db,
        redis_client=redis_client,
    )

    with patch.object(
        auth_service.auth_session_repository,
        "revoke",
    ) as revoke:
        auth_service.logout(None)

        revoke.assert_not_called()


def test_logout_revokes_refresh_session_and_clears_cookie(
    client,
    redis_client,
):
    refresh_token = "test-refresh-token"

    refresh_token_hash = hash_refresh_token(
        refresh_token,
    )

    redis_client.set(
        f"auth:session:{refresh_token_hash}",
        "1",
        ex=300,
    )

    response = client.post(
        "/api/v1/auth/logout",
        cookies={
            "refresh_token": refresh_token,
        },
    )

    assert response.status_code == 204
    assert response.content == b""

    assert (
        redis_client.get(
            f"auth:session:{refresh_token_hash}",
        )
        is None
    )

    set_cookie = response.headers.get("set-cookie")

    assert set_cookie is not None
    assert "refresh_token=" in set_cookie
    assert "Max-Age=0" in set_cookie


def test_login_then_logout(
    client,
    redis_client,
):
    register_response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "logout1@example.com",
            "password": "StrongPassword123!",
            "first_name": "Logout",
            "last_name": "Test",
            "phone": "1234567890",
        },
    )

    assert register_response.status_code == 201

    login_response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "logout1@example.com",
            "password": "StrongPassword123!",
        },
    )

    assert login_response.status_code == 200

    refresh_token = client.cookies.get(
        "refresh_token",
    )

    assert refresh_token is not None

    refresh_token_hash = hash_refresh_token(
        refresh_token,
    )

    assert (
        redis_client.get(
            f"auth:session:{refresh_token_hash}",
        )
        is not None
    )

    logout_response = client.post(
        "/api/v1/auth/logout",
    )

    assert logout_response.status_code == 204
    assert logout_response.content == b""

    assert (
        redis_client.get(
            f"auth:session:{refresh_token_hash}",
        )
        is None
    )
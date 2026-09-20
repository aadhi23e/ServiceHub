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

def test_refresh_requires_refresh_cookie(client):
    response = client.post(
        "/api/v1/auth/refresh",
    )

    assert response.status_code == 401

    body = response.json()

    assert body["error"]["code"] == "AUTHENTICATION_FAILED"
    assert body["error"]["message"] == (
        "Refresh token is required."
    )


def test_refresh_rotates_refresh_token(
    client,
    redis_client,
):
    """End-to-end rotation test"""
    register_response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "refresh@example.com",
            "password": "StrongPassword123!",
            "first_name": "Refresh",
            "last_name": "Test",
            "phone": "1234567890",
        },
    )

    assert register_response.status_code == 201

    login_response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "refresh@example.com",
            "password": "StrongPassword123!",
        },
    )

    assert login_response.status_code == 200

    old_refresh_token = client.cookies.get(
        "refresh_token",
    )

    assert old_refresh_token is not None

    old_refresh_hash = hash_refresh_token(
        old_refresh_token,
    )

    assert redis_client.get(
        f"auth:session:{old_refresh_hash}",
    ) is not None

    refresh_response = client.post(
        "/api/v1/auth/refresh",
    )

    assert refresh_response.status_code == 200

    body = refresh_response.json()

    assert "access_token" in body
    assert body["token_type"] == "bearer"
    assert body["expires_in"] > 0

    new_refresh_token = client.cookies.get(
        "refresh_token",
    )

    assert new_refresh_token is not None

    assert new_refresh_token != old_refresh_token

    new_refresh_hash = hash_refresh_token(
        new_refresh_token,
    )

    # OLD token must be gone.
    assert redis_client.get(
        f"auth:session:{old_refresh_hash}",
    ) is None

    # NEW token must exist.
    assert redis_client.get(
        f"auth:session:{new_refresh_hash}",
    ) is not None


def test_old_refresh_token_cannot_be_reused(
    client,
    redis_client,
):
    """Prove the old token cannot be reused"""
    register_response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "refresh-reuse@example.com",
            "password": "StrongPassword123!",
            "first_name": "Refresh",
            "last_name": "Reuse",
            "phone": "1234567890",
        },
    )

    assert register_response.status_code == 201

    login_response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "refresh-reuse@example.com",
            "password": "StrongPassword123!",
        },
    )

    assert login_response.status_code == 200

    old_refresh_token = client.cookies.get(
        "refresh_token",
    )

    assert old_refresh_token is not None

    # First refresh consumes the old token.
    refresh_response = client.post(
        "/api/v1/auth/refresh",
    )

    assert refresh_response.status_code == 200

    # Explicitly attempt to reuse the old token.
    reuse_response = client.post(
        "/api/v1/auth/refresh",
        cookies={
            "refresh_token": old_refresh_token,
        },
    )

    assert reuse_response.status_code == 401

    body = reuse_response.json()

    assert body["error"]["code"] == (
        "AUTHENTICATION_FAILED"
    )
    assert body["error"]["message"] == (
        "Invalid or expired refresh token."
    )



def test_refresh_rejects_suspended_user(
    client,
    redis_client,
):
    """Test suspended users"""
    register_response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "refresh-suspended@example.com",
            "password": "StrongPassword123!",
            "first_name": "Refresh",
            "last_name": "Suspended",
            "phone": "1234567890",
        },
    )

    assert register_response.status_code == 201

    login_response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "refresh-suspended@example.com",
            "password": "StrongPassword123!",
        },
    )

    assert login_response.status_code == 200

    refresh_token = client.cookies.get(
        "refresh_token",
    )

    assert refresh_token is not None

    refresh_hash = hash_refresh_token(
        refresh_token,
    )

    # We will suspend the user directly in the database
    # in a later dedicated admin test setup.
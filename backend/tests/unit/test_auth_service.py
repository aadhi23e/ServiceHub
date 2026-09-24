from unittest.mock import Mock, patch

import pytest

from app.core.exceptions import AuthenticationError
from app.core.security import hash_refresh_token
from app.enums.user import UserRole, UserStatus
from app.models.user import User
from app.schemas.auth import TokenResponse
from app.services.auth_service import AuthService


def test_refresh_rotates_refresh_token():
    db = Mock()
    redis_client = Mock()

    auth_service = AuthService(
        db=db,
        redis_client=redis_client,
    )

    user = User(
        id=1,
        email="user@example.com",
        password_hash="hashed-password",
        first_name="Test",
        last_name="User",
        role=UserRole.CUSTOMER.value,
        status=UserStatus.ACTIVE.value,
    )

    old_refresh_token = "old-refresh-token"
    new_refresh_token = "new-refresh-token"

    with (
        patch.object(
            auth_service.user_repository,
            "get_by_id",
            return_value=user,
        ) as get_by_id,
        patch.object(
            auth_service.auth_session_repository,
            "consume",
            return_value=user.id,
        ) as consume,
        patch.object(
            auth_service.auth_session_repository,
            "create",
        ) as create,
        patch(
            "app.services.auth_service.create_access_token",
            return_value=("new-access-token", 900),
        ),
        patch(
            "app.services.auth_service.generate_refresh_token",
            return_value=new_refresh_token,
        ),
    ):
        token_response, returned_refresh_token = auth_service.refresh(
            old_refresh_token,
        )

    assert isinstance(
        token_response,
        TokenResponse,
    )

    assert token_response.access_token == "new-access-token"
    assert token_response.token_type == "bearer"
    assert token_response.expires_in == 900

    assert returned_refresh_token == new_refresh_token

    consume.assert_called_once_with(
        hash_refresh_token(old_refresh_token),
    )

    get_by_id.assert_called_once_with(
        user.id,
    )

    create.assert_called_once()

    create_kwargs = create.call_args.kwargs

    assert create_kwargs["user_id"] == user.id
    assert create_kwargs["token_hash"] == hash_refresh_token(
        new_refresh_token,
    )


def test_refresh_rejects_invalid_refresh_token():
    db = Mock()
    redis_client = Mock()

    auth_service = AuthService(
        db=db,
        redis_client=redis_client,
    )

    with patch.object(
        auth_service.auth_session_repository,
        "consume",
        return_value=None,
    ) as consume:
        with pytest.raises(AuthenticationError):
            auth_service.refresh(
                "invalid-refresh-token",
            )

    consume.assert_called_once_with(
        hash_refresh_token(
            "invalid-refresh-token",
        ),
    )


def test_refresh_rejects_missing_user():
    db = Mock()
    redis_client = Mock()

    auth_service = AuthService(
        db=db,
        redis_client=redis_client,
    )

    refresh_token = "refresh-token"

    with (
        patch.object(
            auth_service.auth_session_repository,
            "consume",
            return_value=123,
        ),
        patch.object(
            auth_service.user_repository,
            "get_by_id",
            return_value=None,
        ),
    ):
        with pytest.raises(AuthenticationError):
            auth_service.refresh(
                refresh_token,
            )


def test_refresh_rejects_suspended_user():
    db = Mock()
    redis_client = Mock()

    auth_service = AuthService(
        db=db,
        redis_client=redis_client,
    )

    user = User(
        id=1,
        email="user@example.com",
        password_hash="hashed-password",
        first_name="Test",
        last_name="User",
        role=UserRole.CUSTOMER.value,
        status=UserStatus.SUSPENDED.value,
    )

    with (
        patch.object(
            auth_service.auth_session_repository,
            "consume",
            return_value=user.id,
        ),
        patch.object(
            auth_service.user_repository,
            "get_by_id",
            return_value=user,
        ),
    ):
        with pytest.raises(AuthenticationError):
            auth_service.refresh(
                "refresh-token",
            )

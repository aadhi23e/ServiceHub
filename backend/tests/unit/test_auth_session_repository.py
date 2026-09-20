from unittest.mock import Mock

from app.repositories.auth_session_repository import (
    AuthSessionRepository,
)


def test_consume_returns_user_id_and_deletes_session():
    redis_client = Mock()

    redis_client.getdel.return_value = "123"

    repository = AuthSessionRepository(
        redis_client=redis_client,
    )

    token_hash = "test-token-hash"

    user_id = repository.consume(
        token_hash,
    )

    assert user_id == 123

    redis_client.getdel.assert_called_once_with(
        "auth:session:test-token-hash",
    )


def test_consume_returns_none_when_session_does_not_exist():
    redis_client = Mock()

    redis_client.getdel.return_value = None

    repository = AuthSessionRepository(
        redis_client=redis_client,
    )

    token_hash = "missing-token-hash"

    user_id = repository.consume(
        token_hash,
    )

    assert user_id is None

    redis_client.getdel.assert_called_once_with(
        "auth:session:missing-token-hash",
    )
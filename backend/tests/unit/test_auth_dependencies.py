import pytest

from app.api.dependencies.auth import get_current_token
from app.core.exceptions import AuthenticationError


def test_missing_credentials_rejected() -> None:
    with pytest.raises(AuthenticationError):
        get_current_token(None)
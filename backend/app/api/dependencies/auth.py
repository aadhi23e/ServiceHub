from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.exceptions import AuthenticationError
from app.core.security import decode_access_token

bearer_scheme = HTTPBearer(auto_error=False)


def get_current_token(
    credentials: Annotated[
        HTTPAuthorizationCredentials | None,
        Depends(bearer_scheme),
    ],
) -> str:
    if credentials is None:
        raise AuthenticationError(
            message="Authentication is required.",
        )

    if credentials.scheme.lower() != "bearer":
        raise AuthenticationError(
            message="Authentication is required.",
        )

    return credentials.credentials


def get_current_user_payload(
    token: Annotated[str, Depends(get_current_token)],
) -> dict:
    return decode_access_token(token)
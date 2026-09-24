from typing import Annotated, Any

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from redis import Redis
from sqlalchemy.orm import Session

from app.core.exceptions import AuthenticationError
from app.core.security import decode_access_token
from app.services.auth_service import AuthService
from app.core.redis import get_redis
from app.db.session import get_db

from app.repositories.user_repository import UserRepository
from app.enums.user import UserStatus
from app.dependencies.core import DBSession

bearer_scheme = HTTPBearer(auto_error=False)


def get_auth_service(
    db: Annotated[Session, Depends(get_db)],
    redis_client: Annotated[Redis, Depends(get_redis)],
) -> AuthService:
    return AuthService(
        db=db,
        redis_client=redis_client,
    )


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
) -> dict[str, Any]:
    return decode_access_token(token)


def get_current_user(
    payload: Annotated[
        dict[str, Any],
        Depends(get_current_user_payload),
    ],
    db: DBSession,
):
    user_id = int(payload["sub"])

    user_repository = UserRepository(db)

    user = user_repository.get_by_id(
        user_id,
    )

    if user is None:
        raise AuthenticationError(
            message="User account could not be found.",
        )

    if user.status != UserStatus.ACTIVE.value:
        raise AuthenticationError(
            message="User account is not active.",
        )

    return user

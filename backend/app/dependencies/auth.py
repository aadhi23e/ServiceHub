from typing import Annotated

from redis import Redis
from sqlalchemy.orm import Session

from app.services.auth_service import AuthService
from app.core.redis import get_redis
from app.db.session import get_db

from app.dependencies.core import DBSession

from uuid import UUID

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.security import decode_access_token
from app.dependencies.core import DBSession
# from app.exceptions.authentication import AuthenticationError
from app.core.exceptions import AuthenticationError
from app.models.user import User
from app.repositories.auth_repository import AuthRepository


bearer_scheme = HTTPBearer(auto_error=False)


# Return the authentication service dependency.
def get_auth_service(
    db: Annotated[Session, Depends(get_db)],
    redis_client: Annotated[Redis, Depends(get_redis)],
) -> AuthService:
    return AuthService(
        db=db,
        redis_client=redis_client,
    )

# Extract the Bearer access token from the request.
def get_current_token(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> str:
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise AuthenticationError(
            message="Authentication required."
        )

    return credentials.credentials


# Decode the access token and return its payload.
def get_current_user_payload(
    token: str = Depends(get_current_token),
) -> dict:
    return decode_access_token(token)


# Resolve the authenticated user from the JWT subject.
def get_current_user(
    db: DBSession,
    payload: dict = Depends(get_current_user_payload),
) -> User:
    subject = payload.get("sub")

    if not subject:
        raise AuthenticationError(
            message="Invalid access token."
        )

    try:
        user_id = UUID(subject)
    except (ValueError, TypeError) as exc:
        raise AuthenticationError(
            message="Invalid access token."
        ) from exc

    user = AuthRepository(db).get_user_by_id(user_id)

    if user is None:
        raise AuthenticationError(
            message="User not found."
        )

    if user.status.value != "ACTIVE":
        raise AuthenticationError(
            message="User account is not active."
        )

    return user
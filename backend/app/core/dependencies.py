from typing import Annotated

from fastapi import Depends
from redis import Redis
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.core.redis import get_redis
from app.services.auth_service import AuthService


def get_auth_service(
    db: Annotated[Session, Depends(get_db)],
    redis_client: Annotated[Redis, Depends(get_redis)],
) -> AuthService:
    return AuthService(
        db=db,
        redis_client=redis_client,
    )
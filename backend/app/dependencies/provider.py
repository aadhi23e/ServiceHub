from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.exceptions import AuthorizationError, ResourceNotFoundError
from app.dependencies.auth import get_current_user
from app.dependencies.core import DBSession
from app.enums.user import UserRole
from app.models.provider import ProviderProfile
from app.models.user import User
from app.repositories.provider_repository import ProviderRepository


def get_current_provider(
    current_user: Annotated[User, Depends(get_current_user)],
    db: DBSession,
) -> ProviderProfile:
    if current_user.role != UserRole.PROVIDER.value:
        raise AuthorizationError(
            message="Provider access is required.",
            code="PROVIDER_ACCESS_REQUIRED",
        )

    provider_repository = ProviderRepository(db)

    provider = provider_repository.get_by_user_id(current_user.id)

    if provider is None:
        raise ResourceNotFoundError(
            message="Provider profile not found.",
            code="PROVIDER_PROFILE_NOT_FOUND",
        )

    if provider.status != "ACTIVE":
        raise AuthorizationError(
            message="Your provider account is not active.",
            code="PROVIDER_ACCOUNT_INACTIVE",
        )

    return provider

# from typing import Annotated

# from fastapi import Depends
# from sqlalchemy.orm import Session

# from app.core.exceptions import AuthorizationError, ResourceNotFoundError
# from app.dependencies.auth import get_current_user
# from app.dependencies.core import DBSession
# from app.enums.user import UserRole
# from app.models.provider import ProviderProfile
# from app.models.user import User
# from app.repositories.provider_repository import ProviderRepository


# def get_current_provider(
#     current_user: Annotated[User, Depends(get_current_user)],
#     db: DBSession,
# ) -> ProviderProfile:
#     if current_user.role != UserRole.PROVIDER.value:
#         raise AuthorizationError(
#             message="Provider access is required.",
#             code="PROVIDER_ACCESS_REQUIRED",
#         )

#     provider_repository = ProviderRepository(db)

#     provider = provider_repository.get_by_user_id(current_user.id)

#     if provider is None:
#         raise ResourceNotFoundError(
#             message="Provider profile not found.",
#             code="PROVIDER_PROFILE_NOT_FOUND",
#         )

#     if provider.status != "ACTIVE":
#         raise AuthorizationError(
#             message="Your provider account is not active.",
#             code="PROVIDER_ACCOUNT_INACTIVE",
#         )

#     return provider
from uuid import UUID

from fastapi import Depends

from app.dependencies.core import DBSession
from app.dependencies.auth import get_current_user
from app.enums.user import UserRole
from app.enums.provider import (
    MembershipStatus,
    ProviderMembershipRole,
)
# TODO: need to move the exception from core to new foler exceptoin
# from app.exceptions.authorization import AuthorizationError
# from app.core.exceptions.not_found import ResourceNotFoundError
from app.core.exceptions import AuthorizationError
from app.models.provider_membership import ProviderMembership
from app.core.exceptions import ResourceNotFoundError
from app.models.user import User
from app.repositories.provider_organization_repository import (
    ProviderOrganizationRepository,
)


# Return the active membership for the current user in an organization.
def get_current_organization_membership(
    organization_id: UUID,
    db: DBSession,
    current_user: User = Depends(get_current_user),
) -> ProviderMembership:
    if current_user.role != UserRole.PROVIDER:
        raise AuthorizationError(
            message="Provider access is required."
        )

    repository = ProviderOrganizationRepository(db)

    membership = repository.get_membership(
        user_id=current_user.id,
        organization_id=organization_id,
    )

    if membership is None:
        raise ResourceNotFoundError(
            message="Organization membership not found."
        )

    if membership.status != MembershipStatus.ACTIVE:
        raise AuthorizationError(
            message="Your organization membership is not active."
        )

    return membership


# Require an active organization member.
def require_organization_member(
    membership: ProviderMembership = Depends(
        get_current_organization_membership
    ),
) -> ProviderMembership:
    return membership


# Require an active organization owner or manager.
def require_organization_manager(
    membership: ProviderMembership = Depends(
        get_current_organization_membership
    ),
) -> ProviderMembership:
    if membership.role not in {
        ProviderMembershipRole.OWNER,
        ProviderMembershipRole.MANAGER,
    }:
        raise AuthorizationError(
            message="Owner or manager access is required."
        )

    return membership


# Require an active organization owner.
def require_organization_owner(
    membership: ProviderMembership = Depends(
        get_current_organization_membership
    ),
) -> ProviderMembership:
    if membership.role != ProviderMembershipRole.OWNER:
        raise AuthorizationError(
            message="Organization owner access is required."
        )

    return membership
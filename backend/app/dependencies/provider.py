from fastapi import Depends

from app.dependencies.auth import get_current_user
from app.dependencies.core import DBSession
from app.enums.user import UserRole
from app.enums.provider import (
    MembershipStatus,
    ProviderMembershipRole,
)
from app.core.exceptions import AuthorizationError
from app.core.exceptions import ResourceNotFoundError
from app.models.provider_membership import ProviderMembership
from app.models.user import User
from app.repositories.provider_organization_repository import (
    ProviderOrganizationRepository,
)


# Get the authenticated provider's active organization membership.
def get_current_provider_membership(
    db: DBSession,
    current_user: User = Depends(get_current_user),
) -> ProviderMembership:
    if current_user.role != UserRole.PROVIDER:
        raise AuthorizationError(
            message="Provider access is required.",
        )

    repository = ProviderOrganizationRepository(db)

    membership = repository.get_active_membership_by_user(
        user_id=current_user.id,
    )

    if membership is None:
        raise ResourceNotFoundError(
            message="Active provider organization membership not found.",
        )

    return membership


# Require any active provider organization member.
def require_provider_member(
    membership: ProviderMembership = Depends(
        get_current_provider_membership,
    ),
) -> ProviderMembership:
    return membership


# Require an active owner or manager.
def require_provider_manager(
    membership: ProviderMembership = Depends(
        get_current_provider_membership,
    ),
) -> ProviderMembership:
    if membership.role not in {
        ProviderMembershipRole.OWNER,
        ProviderMembershipRole.MANAGER,
    }:
        raise AuthorizationError(
            message="Owner or manager access is required.",
        )

    return membership


# Require the organization owner.
def require_provider_owner(
    membership: ProviderMembership = Depends(
        get_current_provider_membership,
    ),
) -> ProviderMembership:
    if membership.role != ProviderMembershipRole.OWNER:
        raise AuthorizationError(
            message="Organization owner access is required.",
        )

    return membership
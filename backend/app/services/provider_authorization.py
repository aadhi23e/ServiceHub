from uuid import UUID

from app.enums.provider import (
    MembershipStatus,
    ProviderMembershipRole,
)
from app.core.exceptions import AuthorizationError
from app.models.user import User
from app.repositories.provider_membership import (
    ProviderMembershipRepository,
)


class ProviderAuthorizationService:
    def __init__(
        self,
        membership_repository: ProviderMembershipRepository,
    ):
        self.memberships = membership_repository

    def get_membership(
        self,
        *,
        user_id: UUID,
        organization_id: UUID,
    ):
        membership = (
            self.memberships.get_active_by_user_and_org(
                user_id=user_id,
                organization_id=organization_id,
            )
        )

        if membership is None:
            raise AuthorizationError(
                message="You are not a member of this organization.",
            )

        return membership

    def require_manager_or_owner(
        self,
        *,
        user_id: UUID,
        organization_id: UUID,
    ):
        membership = self.get_membership(
            user_id=user_id,
            organization_id=organization_id,
        )

        if membership.role not in {
            ProviderMembershipRole.OWNER,
            ProviderMembershipRole.MANAGER,
        }:
            raise AuthorizationError(
                message=(
                    "Only the organization owner or a manager "
                    "can perform this operation."
                ),
            )

        return membership

    def require_owner(
        self,
        *,
        user_id: UUID,
        organization_id: UUID,
    ):
        membership = self.get_membership(
            user_id=user_id,
            organization_id=organization_id,
        )

        if membership.role != ProviderMembershipRole.OWNER:
            raise AuthorizationError(
                message=(
                    "Only the organization owner "
                    "can perform this operation."
                ),
            )

        return membership

    def can_manage_target_role(
        self,
        *,
        actor_role: ProviderMembershipRole,
        target_role: ProviderMembershipRole,
    ) -> bool:

        if target_role == ProviderMembershipRole.OWNER:
            return False

        if actor_role == ProviderMembershipRole.OWNER:
            return target_role in {
                ProviderMembershipRole.MANAGER,
                ProviderMembershipRole.AGENT,
            }

        if actor_role == ProviderMembershipRole.MANAGER:
            return target_role == ProviderMembershipRole.AGENT

        return False
from uuid import UUID

from app.enums.user import UserRole, UserStatus
from app.enums.provider import (
    AgentType,
    MembershipStatus,
    ProviderMembershipRole,
    ProviderStatus,
)
from app.core.exceptions import AuthorizationError
from app.core.exceptions import ResourceNotFoundError
from app.models.user import User
from app.repositories.provider_membership import (
    ProviderMembershipRepository,
)
# from app.repositories.provider_organization import (
#     ProviderOrganizationRepository,
# )
from sqlalchemy import select


class ProviderMembershipService:
    def __init__(
        self,
        db,
        membership_repository,
        organization_repository,
    ):
        self.db = db
        self.memberships = membership_repository
        self.organizations = organization_repository

    def add_member(
        self,
        *,
        actor_user_id: UUID,
        organization_id: UUID,
        user_id: UUID,
        role: ProviderMembershipRole,
        agent_type: AgentType | None,
    ):

        organization = self.organizations.get_by_id(
            organization_id
        )

        if organization is None:
            raise ResourceNotFoundError(
                message="Organization not found.",
            )

        if organization.status != ProviderStatus.ACTIVE:
            raise AuthorizationError(
                message=(
                    "The organization is not active."
                ),
            )

        actor = self.memberships.get_active_by_user_and_org(
            user_id=actor_user_id,
            organization_id=organization_id,
        )

        if actor is None:
            raise AuthorizationError(
                message=(
                    "You are not a member of this organization."
                ),
            )

        if actor.role not in {
            ProviderMembershipRole.OWNER,
            ProviderMembershipRole.MANAGER,
        }:
            raise AuthorizationError(
                message=(
                    "Only the owner or a manager "
                    "can add organization members."
                ),
            )

        if (
            actor.role == ProviderMembershipRole.MANAGER
            and role != ProviderMembershipRole.AGENT
        ):
            raise AuthorizationError(
                message=(
                    "Managers can only add agents."
                ),
            )

        if role == ProviderMembershipRole.AGENT:
            if agent_type is None:
                raise ValueError(
                    "Agent type is required for agents."
                )
        else:
            if agent_type is not None:
                raise ValueError(
                    "Agent type is only valid for agents."
                )

        statement = select(User).where(
            User.id == user_id,
        )

        user = self.db.scalar(statement)

        if user is None:
            raise ResourceNotFoundError(
                message="User not found.",
            )

        if user.status != UserStatus.ACTIVE:
            raise AuthorizationError(
                message=(
                    "Only active users can be added "
                    "to an organization."
                ),
            )

        if user.role != UserRole.PROVIDER:
            raise AuthorizationError(
                message=(
                    "Only provider users can become "
                    "organization members."
                ),
            )

        existing = (
            self.memberships.get_any_by_user_and_org(
                user_id=user_id,
                organization_id=organization_id,
            )
        )

        if existing is not None:
            if existing.status != MembershipStatus.REMOVED:
                raise AuthorizationError(
                    message=(
                        "The user is already a member "
                        "of this organization."
                    ),
                )

            existing.status = MembershipStatus.ACTIVE
            existing.role = role
            existing.agent_type = agent_type
            existing.removed_at = None
            existing.joined_at = __import__(
                "datetime"
            ).datetime.now(
                __import__("datetime").timezone.utc
            )

            self.db.flush()

            return existing

        return self.memberships.create(
            user_id=user_id,
            organization_id=organization_id,
            role=role,
            agent_type=agent_type,
        )

    def update_member(
        self,
        *,
        actor_user_id: UUID,
        organization_id: UUID,
        membership_id: UUID,
        role=None,
        agent_type=None,
    ):

        actor = self.memberships.get_active_by_user_and_org(
            user_id=actor_user_id,
            organization_id=organization_id,
        )

        if actor is None:
            raise AuthorizationError(
                message="You are not a member of this organization.",
            )

        if actor.role not in {
            ProviderMembershipRole.OWNER,
            ProviderMembershipRole.MANAGER,
        }:
            raise AuthorizationError(
                message=(
                    "Only the owner or manager "
                    "can update members."
                ),
            )

        membership = self.memberships.get_by_id(
            membership_id
        )

        if (
            membership is None
            or membership.organization_id != organization_id
            or membership.status != MembershipStatus.ACTIVE
        ):
            raise ResourceNotFoundError(
                message="Organization member not found.",
            )

        if membership.role == ProviderMembershipRole.OWNER:
            raise AuthorizationError(
                message="The organization owner cannot be modified.",
            )

        new_role = role or membership.role

        if (
            actor.role == ProviderMembershipRole.MANAGER
            and new_role != ProviderMembershipRole.AGENT
        ):
            raise AuthorizationError(
                message="Managers can only manage agents.",
            )

        if new_role == ProviderMembershipRole.AGENT:
            if agent_type is None:
                agent_type = membership.agent_type

            if agent_type is None:
                raise ValueError(
                    "Agent type is required for agents."
                )
        else:
            agent_type = None

        return self.memberships.update(
            membership,
            role=new_role,
            agent_type=agent_type,
        )

    def remove_member(
        self,
        *,
        actor_user_id: UUID,
        organization_id: UUID,
        membership_id: UUID,
    ):

        actor = self.memberships.get_active_by_user_and_org(
            user_id=actor_user_id,
            organization_id=organization_id,
        )

        if actor is None:
            raise AuthorizationError(
                message="You are not a member of this organization.",
            )

        membership = self.memberships.get_by_id(
            membership_id
        )

        if (
            membership is None
            or membership.organization_id != organization_id
            or membership.status != MembershipStatus.ACTIVE
        ):
            raise ResourceNotFoundError(
                message="Organization member not found.",
            )

        if membership.role == ProviderMembershipRole.OWNER:
            raise AuthorizationError(
                message="The organization owner cannot be removed.",
            )

        if actor.role == ProviderMembershipRole.MANAGER:
            if membership.role != ProviderMembershipRole.AGENT:
                raise AuthorizationError(
                    message=(
                        "Managers can only remove agents."
                    ),
                )

        if actor.role not in {
            ProviderMembershipRole.OWNER,
            ProviderMembershipRole.MANAGER,
        }:
            raise AuthorizationError(
                message=(
                    "Only the owner or manager "
                    "can remove members."
                ),
            )

        return self.memberships.remove(
            membership
        )
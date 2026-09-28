from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy.orm import Session

from app.enums.provider import (
    AgentType,
    MembershipStatus,
    ProviderMembershipRole,
)
from app.core.exceptions import AuthorizationError
from app.core.exceptions import ConflictError
from app.core.exceptions import ResourceNotFoundError
from app.models.provider_membership import ProviderMembership
from app.models.user import User
from app.repositories.provider_membership_repository import (
    ProviderMembershipRepository,
)
from app.schemas.provider_membership import (
    ProviderMemberInvitationCreate,
    ProviderMembershipUpdate,
)


class ProviderMembershipService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = ProviderMembershipRepository(db)

    # Return all members of the provider organization.
    def list_members(
        self,
        organization_id: UUID,
    ) -> list[tuple[ProviderMembership, User]]:
        return self.repository.list_by_organization(
            organization_id=organization_id,
        )

    # Create an invitation for a new organization member.
    def invite_member(
        self,
        organization_id: UUID,
        actor: ProviderMembership,
        data: ProviderMemberInvitationCreate,
    ) -> ProviderMembership:
        self._validate_management_permission(
            actor=actor,
            target_role=data.role,
        )

        user = self._get_user_by_email(data.email)

        if user is None:
            raise ResourceNotFoundError(
                message="User account not found.",
            )

        existing_membership = (
            self.repository.get_by_user_and_organization(
                user_id=user.id,
                organization_id=organization_id,
            )
        )

        if existing_membership is not None:
            raise ConflictError(
                message="User is already a member of this organization.",
            )

        membership = ProviderMembership(
            user_id=user.id,
            organization_id=organization_id,
            role=data.role,
            agent_type=self._validate_agent_type(
                role=data.role,
                agent_type=data.agent_type,
            ),
            status=MembershipStatus.INVITED,
            invited_at=datetime.now(timezone.utc),
        )

        return self.repository.create(membership)

    # Update an existing organization member.
    def update_member(
        self,
        organization_id: UUID,
        membership_id: UUID,
        actor: ProviderMembership,
        data: ProviderMembershipUpdate,
    ) -> ProviderMembership:
        membership = self._get_membership(
            organization_id=organization_id,
            membership_id=membership_id,
        )

        self._validate_target_member(
            actor=actor,
            target=membership,
        )

        role = data.role if data.role is not None else membership.role

        agent_type = (
            data.agent_type
            if data.agent_type is not None
            else membership.agent_type
        )

        self._validate_management_permission(
            actor=actor,
            target_role=role,
        )

        membership.role = role
        membership.agent_type = self._validate_agent_type(
            role=role,
            agent_type=agent_type,
        )

        return self.repository.update(membership)

    # Remove an organization member.
    def remove_member(
        self,
        organization_id: UUID,
        membership_id: UUID,
        actor: ProviderMembership,
    ) -> None:
        membership = self._get_membership(
            organization_id=organization_id,
            membership_id=membership_id,
        )

        self._validate_target_member(
            actor=actor,
            target=membership,
        )

        membership.status = MembershipStatus.REMOVED
        membership.removed_at = datetime.now(timezone.utc)

        self.repository.update(membership)

    # Suspend an active organization member.
    def suspend_member(
        self,
        organization_id: UUID,
        membership_id: UUID,
        actor: ProviderMembership,
    ) -> ProviderMembership:
        membership = self._get_membership(
            organization_id=organization_id,
            membership_id=membership_id,
        )

        self._validate_target_member(
            actor=actor,
            target=membership,
        )

        if membership.status != MembershipStatus.ACTIVE:
            raise ConflictError(
                message="Only active members can be suspended.",
            )

        membership.status = MembershipStatus.SUSPENDED

        return self.repository.update(membership)

    # Reactivate a suspended organization member.
    def reactivate_member(
        self,
        organization_id: UUID,
        membership_id: UUID,
        actor: ProviderMembership,
    ) -> ProviderMembership:
        membership = self._get_membership(
            organization_id=organization_id,
            membership_id=membership_id,
        )

        self._validate_target_member(
            actor=actor,
            target=membership,
        )

        if membership.status != MembershipStatus.SUSPENDED:
            raise ConflictError(
                message="Only suspended members can be reactivated.",
            )

        membership.status = MembershipStatus.ACTIVE

        return self.repository.update(membership)

    # Verify that the actor can manage the target role.
    def _validate_management_permission(
        self,
        actor: ProviderMembership,
        target_role: ProviderMembershipRole,
    ) -> None:
        if actor.role == ProviderMembershipRole.OWNER:
            if target_role not in {
                ProviderMembershipRole.MANAGER,
                ProviderMembershipRole.AGENT,
            }:
                raise AuthorizationError(
                    message="Owner can only manage managers and agents.",
                )

            return

        if actor.role == ProviderMembershipRole.MANAGER:
            if target_role != ProviderMembershipRole.AGENT:
                raise AuthorizationError(
                    message="Manager can only manage agents.",
                )

            return

        raise AuthorizationError(
            message="You do not have permission to manage organization members.",
        )

    # Verify that the actor can modify the specific target member.
    def _validate_target_member(
        self,
        actor: ProviderMembership,
        target: ProviderMembership,
    ) -> None:
        if target.role == ProviderMembershipRole.OWNER:
            raise AuthorizationError(
                message="The organization owner cannot be modified.",
            )

        self._validate_management_permission(
            actor=actor,
            target_role=target.role,
        )

    # Get a membership inside the actor's organization.
    def _get_membership(
        self,
        organization_id: UUID,
        membership_id: UUID,
    ) -> ProviderMembership:
        membership = self.repository.get_by_id(
            membership_id=membership_id,
            organization_id=organization_id,
        )

        if membership is None:
            raise ResourceNotFoundError(
                message="Organization membership not found.",
            )

        return membership

    # Find a user by email.
    def _get_user_by_email(
        self,
        email: str,
    ) -> User | None:
        return (
            self.db.query(User)
            .filter(User.email == email)
            .first()
        )

    # Validate the agent type against the membership role.
    def _validate_agent_type(
        self,
        role: ProviderMembershipRole,
        agent_type: AgentType | None,
    ) -> AgentType | None:
        if role == ProviderMembershipRole.AGENT:
            if agent_type is None:
                raise ConflictError(
                    message="Agent type is required for an agent membership.",
                )

            return agent_type

        if agent_type is not None:
            raise ConflictError(
                message="Agent type is only allowed for agent memberships.",
            )

        return None
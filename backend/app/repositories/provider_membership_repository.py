from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.enums.provider import MembershipStatus
from app.models.provider_membership import ProviderMembership
from app.models.user import User


class ProviderMembershipRepository:
    def __init__(self, db: Session):
        self.db = db

    # Get an active membership for a user.
    def get_active_by_user(
        self,
        user_id: UUID,
    ) -> ProviderMembership | None:
        statement = (
            select(ProviderMembership)
            .where(
                ProviderMembership.user_id == user_id,
                ProviderMembership.status == MembershipStatus.ACTIVE,
            )
            .limit(1)
        )

        return self.db.scalar(statement)

    # Get a membership belonging to an organization.
    def get_by_id(
        self,
        membership_id: UUID,
        organization_id: UUID,
    ) -> ProviderMembership | None:
        statement = select(ProviderMembership).where(
            ProviderMembership.id == membership_id,
            ProviderMembership.organization_id == organization_id,
        )

        return self.db.scalar(statement)

    # Get all members belonging to an organization.
    def list_by_organization(
        self,
        organization_id: UUID,
    ) -> list[tuple[ProviderMembership, User]]:
        statement = (
            select(ProviderMembership, User)
            .join(User, User.id == ProviderMembership.user_id)
            .where(
                ProviderMembership.organization_id == organization_id,
            )
            .order_by(
                ProviderMembership.joined_at.asc().nullslast(),
                ProviderMembership.invited_at.asc().nullslast(),
            )
        )

        return list(self.db.execute(statement).all())

    # Find an existing membership for a user in an organization.
    def get_by_user_and_organization(
        self,
        user_id: UUID,
        organization_id: UUID,
    ) -> ProviderMembership | None:
        statement = select(ProviderMembership).where(
            ProviderMembership.user_id == user_id,
            ProviderMembership.organization_id == organization_id,
        )

        return self.db.scalar(statement)

    # Create a new membership.
    def create(
        self,
        membership: ProviderMembership,
    ) -> ProviderMembership:
        self.db.add(membership)
        self.db.flush()

        return membership

    # Update an existing membership.
    def update(
        self,
        membership: ProviderMembership,
    ) -> ProviderMembership:
        self.db.flush()

        return membership

    # Delete a membership.
    def delete(
        self,
        membership: ProviderMembership,
    ) -> None:
        self.db.delete(membership)
        self.db.flush()
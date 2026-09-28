from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.enums.provider import (
    MembershipStatus,
    ProviderMembershipRole,
    ProviderStatus,
)
from app.models.provider_membership import ProviderMembership
from app.models.provider_organization import ProviderOrganization
from app.models.service import Service
from app.models.provider_location import ProviderLocation


class ProviderOrganizationRepository:
    def __init__(self, db: Session):
        self.db = db

    # Return an organization by its primary key.
    def get_by_id(
        self,
        organization_id: UUID,
    ) -> ProviderOrganization | None:
        statement = select(ProviderOrganization).where(
            ProviderOrganization.id == organization_id
        )

        return self.db.scalar(statement)

    # Return an active membership for a user in an organization.
    def get_membership(
        self,
        *,
        user_id: UUID,
        organization_id: UUID,
    ) -> ProviderMembership | None:
        statement = select(ProviderMembership).where(
            ProviderMembership.user_id == user_id,
            ProviderMembership.organization_id == organization_id,
            ProviderMembership.status == MembershipStatus.ACTIVE,
        )

        return self.db.scalar(statement)

    # Return all organizations that the user actively belongs to.
    def list_for_user(
        self,
        *,
        user_id: UUID,
    ) -> list[ProviderOrganization]:
        statement = (
            select(ProviderOrganization)
            .join(
                ProviderMembership,
                ProviderMembership.organization_id
                == ProviderOrganization.id,
            )
            .where(
                ProviderMembership.user_id == user_id,
                ProviderMembership.status == MembershipStatus.ACTIVE,
            )
            .order_by(ProviderOrganization.name.asc())
        )

        return list(self.db.scalars(statement).all())

    # Update organization fields without committing the transaction.
    def update(
        self,
        organization: ProviderOrganization,
        *,
        name: str | None = None,
        legal_name: str | None = None,
        description: str | None = None,
    ) -> ProviderOrganization:
        if name is not None:
            organization.name = name

        if legal_name is not None:
            organization.legal_name = legal_name

        if description is not None:
            organization.description = description

        self.db.flush()

        return organization

    # Change the organization status without committing the transaction.
    def set_status(
        self,
        organization: ProviderOrganization,
        status: ProviderStatus,
    ) -> ProviderOrganization:
        organization.status = status

        self.db.flush()

        return organization

    # Count active members belonging to an organization.
    def count_active_members(
        self,
        organization_id: UUID,
    ) -> int:
        statement = select(func.count()).select_from(
            ProviderMembership
        ).where(
            ProviderMembership.organization_id == organization_id,
            ProviderMembership.status == MembershipStatus.ACTIVE,
        )

        return int(self.db.scalar(statement) or 0)

    # Count active provider locations belonging to an organization.
    def count_active_locations(
        self,
        organization_id: UUID,
    ) -> int:
        statement = select(func.count()).select_from(
            ProviderLocation
        ).where(
            ProviderLocation.organization_id == organization_id,
        )

        return int(self.db.scalar(statement) or 0)

    # Count services belonging to an organization.
    def count_services(
        self,
        organization_id: UUID,
    ) -> int:
        statement = select(func.count()).select_from(
            Service
        ).where(
            Service.organization_id == organization_id,
        )

        return int(self.db.scalar(statement) or 0)
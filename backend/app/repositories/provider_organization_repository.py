from uuid import UUID

from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from app.enums.provider import MembershipStatus, ProviderStatus
from app.models.provider_membership import ProviderMembership
from app.models.provider_organization import ProviderOrganization
from app.models.provider_location import ProviderLocation
from app.models.service import Service


class ProviderOrganizationRepository:
    def __init__(self, db: Session):
        self.db = db

    # Return an organization by ID.
    def get_by_id(
        self,
        organization_id: UUID,
    ) -> ProviderOrganization | None:
        statement = select(ProviderOrganization).where(
            ProviderOrganization.id == organization_id
        )

        return self.db.scalar(statement)

    # Return a public organization by ID.
    def get_public_by_id(
        self,
        organization_id: UUID,
    ) -> ProviderOrganization | None:
        statement = select(ProviderOrganization).where(
            ProviderOrganization.id == organization_id,
            ProviderOrganization.status == ProviderStatus.ACTIVE,
        )

        return self.db.scalar(statement)

    # Return the active membership for a provider user.
    def get_active_membership_by_user(
        self,
        *,
        user_id: UUID,
    ) -> ProviderMembership | None:
        statement = (
            select(ProviderMembership)
            .where(
                ProviderMembership.user_id == user_id,
                ProviderMembership.status == MembershipStatus.ACTIVE,
            )
            .order_by(ProviderMembership.joined_at.asc())
            .limit(1)
        )

        return self.db.scalar(statement)

    # Return all publicly visible organizations.
    def list_public(
        self,
        *,
        search: str | None,
        offset: int,
        limit: int,
    ) -> tuple[list[ProviderOrganization], int]:
        conditions = [
            ProviderOrganization.status == ProviderStatus.ACTIVE,
        ]

        if search:
            search_pattern = f"%{search.strip()}%"

            conditions.append(
                or_(
                    ProviderOrganization.name.ilike(search_pattern),
                    ProviderOrganization.description.ilike(
                        search_pattern
                    ),
                )
            )

        data_statement = (
            select(ProviderOrganization)
            .where(*conditions)
            .order_by(
                ProviderOrganization.name.asc(),
                ProviderOrganization.created_at.desc(),
            )
            .offset(offset)
            .limit(limit)
        )

        count_statement = (
            select(func.count())
            .select_from(ProviderOrganization)
            .where(*conditions)
        )

        organizations = list(
            self.db.scalars(data_statement).all()
        )

        total = int(self.db.scalar(count_statement) or 0)

        return organizations, total

    # Return all organizations for platform administration.
    def list_all(
        self,
        *,
        search: str | None,
        status: ProviderStatus | None,
        offset: int,
        limit: int,
    ) -> tuple[list[ProviderOrganization], int]:
        conditions = []

        if search:
            search_pattern = f"%{search.strip()}%"

            conditions.append(
                or_(
                    ProviderOrganization.name.ilike(search_pattern),
                    ProviderOrganization.legal_name.ilike(
                        search_pattern
                    ),
                    ProviderOrganization.description.ilike(
                        search_pattern
                    ),
                )
            )

        if status is not None:
            conditions.append(
                ProviderOrganization.status == status
            )

        data_statement = (
            select(ProviderOrganization)
            .where(*conditions)
            .order_by(
                ProviderOrganization.created_at.desc()
            )
            .offset(offset)
            .limit(limit)
        )

        count_statement = (
            select(func.count())
            .select_from(ProviderOrganization)
            .where(*conditions)
        )

        organizations = list(
            self.db.scalars(data_statement).all()
        )

        total = int(self.db.scalar(count_statement) or 0)

        return organizations, total

    # Update organization information without committing.
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

    # Change an organization's status without committing.
    def set_status(
        self,
        organization: ProviderOrganization,
        status: ProviderStatus,
    ) -> ProviderOrganization:
        organization.status = status

        self.db.flush()

        return organization

    # Count active organization members.
    def count_active_members(
        self,
        organization_id: UUID,
    ) -> int:
        statement = (
            select(func.count())
            .select_from(ProviderMembership)
            .where(
                ProviderMembership.organization_id
                == organization_id,
                ProviderMembership.status
                == MembershipStatus.ACTIVE,
            )
        )

        return int(self.db.scalar(statement) or 0)

    # Count provider locations belonging to an organization.
    def count_locations(
        self,
        organization_id: UUID,
    ) -> int:
        statement = (
            select(func.count())
            .select_from(ProviderLocation)
            .where(
                ProviderLocation.organization_id
                == organization_id
            )
        )

        return int(self.db.scalar(statement) or 0)

    # Count services belonging to an organization.
    def count_services(
        self,
        organization_id: UUID,
    ) -> int:
        statement = (
            select(func.count())
            .select_from(Service)
            .where(
                Service.organization_id
                == organization_id
            )
        )

        return int(self.db.scalar(statement) or 0)
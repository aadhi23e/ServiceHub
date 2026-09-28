from math import ceil
from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.enums.provider import ProviderStatus
from app.core.exceptions import ConflictError
from app.core.exceptions import ResourceNotFoundError
from app.models.provider_organization import ProviderOrganization
from app.repositories.provider_organization_repository import (
    ProviderOrganizationRepository,
)
from app.schemas.provider_organization import (
    ProviderOrganizationAdminListItem,
    ProviderOrganizationAdminResponse,
    ProviderOrganizationListItem,
    ProviderOrganizationListResponse,
    ProviderOrganizationPublicResponse,
    ProviderOrganizationResponse,
    ProviderOrganizationSummaryResponse,
    ProviderOrganizationUpdateRequest,
)


class ProviderOrganizationService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = ProviderOrganizationRepository(db)

    # Return a public organization.
    def get_public_organization(
        self,
        organization_id: UUID,
    ) -> ProviderOrganizationPublicResponse:
        organization = self.repository.get_public_by_id(
            organization_id
        )

        if organization is None:
            raise ResourceNotFoundError(
                message="Organization not found."
            )

        return ProviderOrganizationPublicResponse.model_validate(
            organization
        )

    # Return publicly visible organizations with pagination.
    def list_public_organizations(
        self,
        *,
        search: str | None,
        page: int,
        page_size: int,
    ) -> ProviderOrganizationListResponse:
        offset = (page - 1) * page_size

        organizations, total = self.repository.list_public(
            search=search,
            offset=offset,
            limit=page_size,
        )

        total_pages = ceil(total / page_size) if total else 0

        items = [
            ProviderOrganizationListItem.model_validate(
                organization
            )
            for organization in organizations
        ]

        return ProviderOrganizationListResponse(
            items=items,
            page=page,
            page_size=page_size,
            total=total,
            total_pages=total_pages,
        )

    # Return the organization belonging to the current provider.
    def get_my_organization(
        self,
        *,
        organization_id: UUID,
    ) -> ProviderOrganizationResponse:
        organization = self.repository.get_by_id(
            organization_id
        )

        if organization is None:
            raise ResourceNotFoundError(
                message="Provider organization not found."
            )

        return ProviderOrganizationResponse.model_validate(
            organization
        )

    # Update provider organization information.
    def update_my_organization(
        self,
        *,
        organization_id: UUID,
        data: ProviderOrganizationUpdateRequest,
    ) -> ProviderOrganizationResponse:
        organization = self.repository.get_by_id(
            organization_id
        )

        if organization is None:
            raise ResourceNotFoundError(
                message="Provider organization not found."
            )

        if organization.status in {
            ProviderStatus.SUSPENDED,
            ProviderStatus.DEACTIVATED,
        }:
            raise ConflictError(
                message=(
                    "A suspended or deactivated organization "
                    "cannot be edited."
                )
            )

        update_data = data.model_dump(
            exclude_unset=True
        )

        if not update_data:
            return ProviderOrganizationResponse.model_validate(
                organization
            )

        try:
            organization = self.repository.update(
                organization,
                **update_data,
            )

            self.db.commit()
            self.db.refresh(organization)

            return ProviderOrganizationResponse.model_validate(
                organization
            )

        except IntegrityError as exc:
            self.db.rollback()

            raise ConflictError(
                message="The organization could not be updated."
            ) from exc

        except Exception:
            self.db.rollback()
            raise

    # Return the complete organization record for platform administration.
    def get_admin_organization(
        self,
        organization_id: UUID,
    ) -> ProviderOrganizationAdminResponse:
        organization = self.repository.get_by_id(
            organization_id
        )

        if organization is None:
            raise ResourceNotFoundError(
                message="Organization not found."
            )

        return ProviderOrganizationAdminResponse.model_validate(
            organization
        )

    # Return all organizations for platform administration.
    def list_admin_organizations(
        self,
        *,
        search: str | None,
        status: ProviderStatus | None,
        page: int,
        page_size: int,
    ) -> list[ProviderOrganizationAdminListItem]:
        offset = (page - 1) * page_size

        organizations, _ = self.repository.list_all(
            search=search,
            status=status,
            offset=offset,
            limit=page_size,
        )

        return [
            ProviderOrganizationAdminListItem.model_validate(
                organization
            )
            for organization in organizations
        ]

    # Return organization operational summary for platform administration.
    def get_admin_summary(
        self,
        organization_id: UUID,
    ) -> ProviderOrganizationSummaryResponse:
        organization = self.repository.get_by_id(
            organization_id
        )

        if organization is None:
            raise ResourceNotFoundError(
                message="Organization not found."
            )

        return ProviderOrganizationSummaryResponse(
            id=organization.id,
            name=organization.name,
            status=organization.status,
            member_count=self.repository.count_active_members(
                organization.id
            ),
            location_count=self.repository.count_locations(
                organization.id
            ),
            service_count=self.repository.count_services(
                organization.id
            ),
        )

    # Deactivate an organization through the platform administration API.
    def deactivate_organization(
        self,
        organization_id: UUID,
    ) -> ProviderOrganization:
        organization = self.repository.get_by_id(
            organization_id
        )

        if organization is None:
            raise ResourceNotFoundError(
                message="Organization not found."
            )

        if organization.status == ProviderStatus.DEACTIVATED:
            raise ConflictError(
                message="Organization is already deactivated."
            )

        if organization.status != ProviderStatus.ACTIVE:
            raise ConflictError(
                message=(
                    "Only an active organization can "
                    "be deactivated."
                )
            )

        try:
            self.repository.set_status(
                organization,
                ProviderStatus.DEACTIVATED,
            )

            self.db.commit()
            self.db.refresh(organization)

            return organization

        except Exception:
            self.db.rollback()
            raise

    # Reactivate an organization through the platform administration API.
    def reactivate_organization(
        self,
        organization_id: UUID,
    ) -> ProviderOrganization:
        organization = self.repository.get_by_id(
            organization_id
        )

        if organization is None:
            raise ResourceNotFoundError(
                message="Organization not found."
            )

        if organization.status == ProviderStatus.ACTIVE:
            raise ConflictError(
                message="Organization is already active."
            )

        if organization.status != ProviderStatus.DEACTIVATED:
            raise ConflictError(
                message=(
                    "Only a deactivated organization can "
                    "be reactivated."
                )
            )

        try:
            self.repository.set_status(
                organization,
                ProviderStatus.ACTIVE,
            )

            self.db.commit()
            self.db.refresh(organization)

            return organization

        except Exception:
            self.db.rollback()
            raise
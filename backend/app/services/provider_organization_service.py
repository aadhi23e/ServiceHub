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
    ProviderOrganizationListItem,
    ProviderOrganizationSummaryResponse,
    ProviderOrganizationUpdateRequest,
)


class ProviderOrganizationService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = ProviderOrganizationRepository(db)

    # Return one organization after verifying it exists.
    def get_organization(
        self,
        organization_id: UUID,
    ) -> ProviderOrganization:
        organization = self.repository.get_by_id(
            organization_id
        )

        if organization is None:
            raise ResourceNotFoundError(
                message="Provider organization not found."
            )

        return organization

    # Return all organizations the current user actively belongs to.
    def list_organizations(
        self,
        *,
        user_id: UUID,
    ) -> list[ProviderOrganizationListItem]:
        organizations = self.repository.list_for_user(
            user_id=user_id,
        )

        return [
            ProviderOrganizationListItem.model_validate(
                organization
            )
            for organization in organizations
        ]

    # Update editable organization information.
    def update_organization(
        self,
        *,
        organization_id: UUID,
        data: ProviderOrganizationUpdateRequest,
    ) -> ProviderOrganization:
        organization = self.get_organization(
            organization_id
        )

        if organization.status in {
            ProviderStatus.SUSPENDED,
            ProviderStatus.DEACTIVATED,
        }:
            raise ConflictError(
                message=(
                    "A suspended or deactivated organization "
                    "cannot be updated."
                )
            )

        update_data = data.model_dump(
            exclude_unset=True,
        )

        if not update_data:
            return organization

        try:
            organization = self.repository.update(
                organization,
                **update_data,
            )

            self.db.commit()
            self.db.refresh(organization)

            return organization

        except IntegrityError as exc:
            self.db.rollback()

            raise ConflictError(
                message="The organization could not be updated."
            ) from exc

        except Exception:
            self.db.rollback()
            raise

    # Return operational summary information for an organization.
    def get_summary(
        self,
        organization_id: UUID,
    ) -> ProviderOrganizationSummaryResponse:
        organization = self.get_organization(
            organization_id
        )

        member_count = self.repository.count_active_members(
            organization_id
        )

        location_count = self.repository.count_active_locations(
            organization_id
        )

        service_count = self.repository.count_services(
            organization_id
        )

        return ProviderOrganizationSummaryResponse(
            id=organization.id,
            name=organization.name,
            status=organization.status,
            member_count=member_count,
            location_count=location_count,
            service_count=service_count,
        )

    # Deactivate an active provider organization.
    def deactivate_organization(
        self,
        organization_id: UUID,
    ) -> ProviderOrganization:
        organization = self.get_organization(
            organization_id
        )

        if organization.status == ProviderStatus.DEACTIVATED:
            raise ConflictError(
                message="Organization is already deactivated."
            )

        if organization.status != ProviderStatus.ACTIVE:
            raise ConflictError(
                message=(
                    "Only an active organization can be "
                    "deactivated."
                )
            )

        try:
            organization = self.repository.set_status(
                organization,
                ProviderStatus.DEACTIVATED,
            )

            self.db.commit()
            self.db.refresh(organization)

            return organization

        except Exception:
            self.db.rollback()
            raise

    # Reactivate a previously deactivated provider organization.
    def reactivate_organization(
        self,
        organization_id: UUID,
    ) -> ProviderOrganization:
        organization = self.get_organization(
            organization_id
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
            organization = self.repository.set_status(
                organization,
                ProviderStatus.ACTIVE,
            )

            self.db.commit()
            self.db.refresh(organization)

            return organization

        except Exception:
            self.db.rollback()
            raise
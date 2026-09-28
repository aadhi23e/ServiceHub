from uuid import UUID

from fastapi import APIRouter, Depends, Query, status

from app.dependencies.core import DBSession
from app.dependencies.provider import (
    require_provider_member,
    require_provider_manager,
)
from app.models.provider_membership import ProviderMembership
from app.schemas.provider_organization import (
    ProviderOrganizationListResponse,
    ProviderOrganizationPublicResponse,
    ProviderOrganizationResponse,
    ProviderOrganizationUpdateRequest,
)
from app.services.provider_organization_service import (
    ProviderOrganizationService,
)

from app.enums.provider import MembershipStatus

router = APIRouter(
    prefix="/organizations",
    tags=["Organizations"],
)


# List all publicly available organizations.
@router.get(
    "",
    response_model=ProviderOrganizationListResponse,
    status_code=status.HTTP_200_OK,
)
def list_organizations(
    db: DBSession,
    search: str | None = Query(
        default=None,
        min_length=1,
        max_length=100,
    ),
    page: int = Query(
        default=1,
        ge=1,
    ),
    page_size: int = Query(
        default=20,
        ge=1,
        le=100,
    ),
) -> ProviderOrganizationListResponse:
    service = ProviderOrganizationService(db)

    return service.list_public_organizations(
        search=search,
        page=page,
        page_size=page_size,
    )


# Return public information about one organization.
@router.get(
    "/{organization_id}",
    response_model=ProviderOrganizationPublicResponse,
    status_code=status.HTTP_200_OK,
)
def get_organization(
    organization_id: UUID,
    db: DBSession,
) -> ProviderOrganizationPublicResponse:
    service = ProviderOrganizationService(db)

    return service.get_public_organization(
        organization_id
    )


# Return the authenticated provider's own organization.
@router.get(
    "/me",
    response_model=ProviderOrganizationResponse,
    status_code=status.HTTP_200_OK,
)
def get_my_organization(
    db: DBSession,
    membership: ProviderMembership = Depends(
        require_provider_member
    ),
) -> ProviderOrganizationResponse:
    service = ProviderOrganizationService(db)

    return service.get_my_organization(
        organization_id=membership.organization_id,
    )


# Update the authenticated provider's organization.
@router.patch(
    "/me",
    response_model=ProviderOrganizationResponse,
    status_code=status.HTTP_200_OK,
)
def update_my_organization(
    data: ProviderOrganizationUpdateRequest,
    db: DBSession,
    membership: ProviderMembership = Depends(
        require_provider_manager
    ),
) -> ProviderOrganizationResponse:
    service = ProviderOrganizationService(db)

    return service.update_my_organization(
        organization_id=membership.organization_id,
        data=data,
    )

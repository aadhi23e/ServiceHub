from uuid import UUID

from fastapi import APIRouter, Query, status

from app.dependencies.core import DBSession
from app.schemas.provider_organization import (
    ProviderOrganizationPublicListResponse,
    ProviderOrganizationPublicResponse,
)
from app.services.provider_organization_service import (
    ProviderOrganizationService,
)


router = APIRouter(
    prefix="/organizations",
    tags=["Organizations"],
)


# List publicly available organizations.
@router.get(
    "",
    response_model=ProviderOrganizationPublicListResponse,
    status_code=status.HTTP_200_OK,
)
def list_organizations(
    db: DBSession,
    search: str | None = Query(
        default=None,
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
) -> ProviderOrganizationPublicListResponse:
    service = ProviderOrganizationService(db)

    organizations, total, total_pages = service.list_public(
        search=search,
        page=page,
        page_size=page_size,
    )

    return ProviderOrganizationPublicListResponse(
        items=organizations,
        page=page,
        page_size=page_size,
        total=total,
        total_pages=total_pages,
    )


# Return one publicly available organization.
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

    return service.get_public(
        organization_id=organization_id,
    )
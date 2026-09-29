from uuid import UUID

from fastapi import APIRouter, Depends, Query, status

from app.dependencies.authorization import require_admin
from app.dependencies.core import DBSession
from app.enums.provider import ProviderStatus
from app.models.user import User
from app.schemas.provider_organization import (
    ProviderOrganizationAdminListItem,
    ProviderOrganizationAdminListResponse,
    ProviderOrganizationAdminResponse,
    ProviderOrganizationAdminSummary,
)
from app.services.provider_organization_service import (
    ProviderOrganizationService,
)


router = APIRouter(
    prefix="/admin/organizations",
    tags=["Admin - Organizations"],
)


# List organizations for platform administration.
@router.get(
    "",
    response_model=ProviderOrganizationAdminListResponse,
    status_code=status.HTTP_200_OK,
)
def list_organizations(
    db: DBSession,
    admin: User = Depends(require_admin),
    search: str | None = Query(
        default=None,
        max_length=100,
    ),
    organization_status: ProviderStatus | None = Query(
        default=None,
        alias="status",
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
) -> ProviderOrganizationAdminListResponse:
    service = ProviderOrganizationService(db)

    organizations, total, total_pages = service.list_admin(
        search=search,
        status=organization_status,
        page=page,
        page_size=page_size,
    )

    items = [
        ProviderOrganizationAdminListItem.model_validate(
            organization,
        )
        for organization in organizations
    ]

    return ProviderOrganizationAdminListResponse(
        items=items,
        page=page,
        page_size=page_size,
        total=total,
        total_pages=total_pages,
    )


# Return full organization information to an administrator.
@router.get(
    "/{organization_id}",
    response_model=ProviderOrganizationAdminResponse,
    status_code=status.HTTP_200_OK,
)
def get_organization(
    organization_id: UUID,
    db: DBSession,
    admin: User = Depends(require_admin),
) -> ProviderOrganizationAdminResponse:
    service = ProviderOrganizationService(db)

    return service.get_admin_organization(
        organization_id=organization_id,
    )


# Return administrative organization statistics.
@router.get(
    "/{organization_id}/summary",
    response_model=ProviderOrganizationAdminSummary,
    status_code=status.HTTP_200_OK,
)
def get_organization_summary(
    organization_id: UUID,
    db: DBSession,
    admin: User = Depends(require_admin),
) -> ProviderOrganizationAdminSummary:
    service = ProviderOrganizationService(db)

    return service.get_admin_summary(
        organization_id=organization_id,
    )


# Deactivate an organization.
@router.post(
    "/{organization_id}/deactivate",
    response_model=ProviderOrganizationAdminResponse,
    status_code=status.HTTP_200_OK,
)
def deactivate_organization(
    organization_id: UUID,
    db: DBSession,
    admin: User = Depends(require_admin),
) -> ProviderOrganizationAdminResponse:
    service = ProviderOrganizationService(db)

    organization = service.deactivate(
        organization_id=organization_id,
    )

    db.commit()
    db.refresh(organization)

    return organization


# Reactivate a deactivated organization.
@router.post(
    "/{organization_id}/reactivate",
    response_model=ProviderOrganizationAdminResponse,
    status_code=status.HTTP_200_OK,
)
def reactivate_organization(
    organization_id: UUID,
    db: DBSession,
    admin: User = Depends(require_admin),
) -> ProviderOrganizationAdminResponse:
    service = ProviderOrganizationService(db)

    organization = service.reactivate(
        organization_id=organization_id,
    )

    db.commit()
    db.refresh(organization)

    return organization
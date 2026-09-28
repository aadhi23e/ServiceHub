from uuid import UUID

from fastapi import APIRouter, Depends, Response, status

from app.dependencies.auth import get_current_user
from app.dependencies.core import DBSession
from app.dependencies.provider import (
    require_organization_manager,
    require_organization_member,
    require_organization_owner,
)
from app.models.provider_membership import ProviderMembership
from app.models.user import User
from app.schemas.provider_organization import (
    ProviderOrganizationListItem,
    ProviderOrganizationResponse,
    ProviderOrganizationSummaryResponse,
    ProviderOrganizationUpdateRequest,
)
from app.services.provider_organization_service import (
    ProviderOrganizationService,
)


router = APIRouter(
    prefix="/providers/organizations",
    tags=["Provider Organizations"],
)


# List all organizations that the authenticated provider belongs to.
@router.get(
    "",
    response_model=list[ProviderOrganizationListItem],
    status_code=status.HTTP_200_OK,
)
def list_organizations(
    db: DBSession,
    current_user: User = Depends(get_current_user),
) -> list[ProviderOrganizationListItem]:
    service = ProviderOrganizationService(db)

    return service.list_organizations(
        user_id=current_user.id,
    )


# Get an organization that the authenticated user belongs to.
@router.get(
    "/{organization_id}",
    response_model=ProviderOrganizationResponse,
    status_code=status.HTTP_200_OK,
)
def get_organization(
    organization_id: UUID,
    db: DBSession,
    membership: ProviderMembership = Depends(
        require_organization_member
    ),
) -> ProviderOrganizationResponse:
    service = ProviderOrganizationService(db)

    organization = service.get_organization(
        organization_id,
    )

    return ProviderOrganizationResponse.model_validate(
        organization
    )


# Update organization information as an owner or manager.
@router.patch(
    "/{organization_id}",
    response_model=ProviderOrganizationResponse,
    status_code=status.HTTP_200_OK,
)
def update_organization(
    organization_id: UUID,
    data: ProviderOrganizationUpdateRequest,
    db: DBSession,
    membership: ProviderMembership = Depends(
        require_organization_manager
    ),
) -> ProviderOrganizationResponse:
    service = ProviderOrganizationService(db)

    organization = service.update_organization(
        organization_id=organization_id,
        data=data,
    )

    return ProviderOrganizationResponse.model_validate(
        organization
    )


# Return operational information about an organization.
@router.get(
    "/{organization_id}/summary",
    response_model=ProviderOrganizationSummaryResponse,
    status_code=status.HTTP_200_OK,
)
def get_organization_summary(
    organization_id: UUID,
    db: DBSession,
    membership: ProviderMembership = Depends(
        require_organization_member
    ),
) -> ProviderOrganizationSummaryResponse:
    service = ProviderOrganizationService(db)

    return service.get_summary(
        organization_id,
    )


# Deactivate an organization as its owner.
@router.post(
    "/{organization_id}/deactivate",
    response_model=ProviderOrganizationResponse,
    status_code=status.HTTP_200_OK,
)
def deactivate_organization(
    organization_id: UUID,
    db: DBSession,
    membership: ProviderMembership = Depends(
        require_organization_owner
    ),
) -> ProviderOrganizationResponse:
    service = ProviderOrganizationService(db)

    organization = service.deactivate_organization(
        organization_id,
    )

    return ProviderOrganizationResponse.model_validate(
        organization
    )


# Reactivate a deactivated organization as its owner.
@router.post(
    "/{organization_id}/reactivate",
    response_model=ProviderOrganizationResponse,
    status_code=status.HTTP_200_OK,
)
def reactivate_organization(
    organization_id: UUID,
    db: DBSession,
    membership: ProviderMembership = Depends(
        require_organization_owner
    ),
) -> ProviderOrganizationResponse:
    service = ProviderOrganizationService(db)

    organization = service.reactivate_organization(
        organization_id,
    )

    return ProviderOrganizationResponse.model_validate(
        organization
    )
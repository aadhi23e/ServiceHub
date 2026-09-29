from fastapi import APIRouter, Depends, status

from app.dependencies.core import DBSession
from app.dependencies.provider import (
    get_current_provider_membership,
    require_provider_manager,
)
from app.models.provider_membership import ProviderMembership
from app.schemas.provider_organization import (
    ProviderOrganizationResponse,
    ProviderOrganizationUpdate,
)
from app.services.provider_organization_service import (
    ProviderOrganizationService,
)


router = APIRouter(
    prefix="/organizations/me",
    tags=["My Organization"],
)


# Return the authenticated provider's organization.
@router.get(
    "",
    response_model=ProviderOrganizationResponse,
    status_code=status.HTTP_200_OK,
)
def get_my_organization(
    db: DBSession,
    membership: ProviderMembership = Depends(
        get_current_provider_membership,
    ),
) -> ProviderOrganizationResponse:
    service = ProviderOrganizationService(db)

    return service.get_my_organization(
        membership=membership,
    )


# Update the authenticated provider's organization.
@router.patch(
    "",
    response_model=ProviderOrganizationResponse,
    status_code=status.HTTP_200_OK,
)
def update_my_organization(
    data: ProviderOrganizationUpdate,
    db: DBSession,
    membership: ProviderMembership = Depends(
        require_provider_manager,
    ),
) -> ProviderOrganizationResponse:
    service = ProviderOrganizationService(db)

    organization = service.update_my_organization(
        membership=membership,
        data=data,
    )

    db.commit()
    db.refresh(organization)

    return organization
from fastapi import APIRouter, Depends, status

from app.dependencies.auth import get_current_user
from app.dependencies.core import DBSession
from app.enums.user import UserRole
from app.core.exceptions import AuthorizationError
from app.models.user import User
from app.schemas.provider_organization import (
    ProviderOrganizationCreate,
    ProviderOrganizationResponse,
)
from app.services.provider_organization_service import (
    ProviderOrganizationService,
)


router = APIRouter(
    prefix="/provider/organizations",
    tags=["Provider Organizations"],
)


# Create a provider organization for the authenticated customer.
@router.post(
    "",
    response_model=ProviderOrganizationResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_provider_organization(
    data: ProviderOrganizationCreate,
    db: DBSession,
    current_user: User = Depends(get_current_user),
) -> ProviderOrganizationResponse:
    if current_user.role != UserRole.CUSTOMER:
        raise AuthorizationError(
            message="Only customer accounts can create a provider organization.",
        )

    service = ProviderOrganizationService(db)

    try:
        organization = service.create_provider_organization(
            user=current_user,
            data=data,
        )

        db.commit()
        db.refresh(current_user)
        db.refresh(organization)
    
    
    except Exception:
        db.rollback()
        raise
    
    return organization
    
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status

from app.dependencies.authorization import get_current_user
from app.dependencies.core import DBSession
from app.models.user import User
from app.repositories.provider_membership import (
    ProviderMembershipRepository,
)
from app.repositories.provider_service_offering import (
    ProviderServiceOfferingRepository,
)
from app.repositories.service import ServiceRepository
from app.schemas.provider_service_offering import (
    ProviderServiceOfferingCreateRequest,
    ProviderServiceOfferingListResponse,
    ProviderServiceOfferingResponse,
    ProviderServiceOfferingUpdateRequest,
)
from app.services.provider_service_offering import (
    ProviderServiceOfferingService,
)

router = APIRouter(
    prefix="/provider/service-offerings",
    tags=["Provider Service Offerings"],
)


def get_provider_service_offering_service(
    db: DBSession,
) -> ProviderServiceOfferingService:
    return ProviderServiceOfferingService(
        db=db,
        offering_repo=ProviderServiceOfferingRepository(db),
        membership_repo=ProviderMembershipRepository(db),
        service_repo=ServiceRepository(db),
    )


@router.get(
    "",
    response_model=ProviderServiceOfferingListResponse,
)
def list_service_offerings(
    page: int = Query(
        default=1,
        ge=1,
    ),
    page_size: int = Query(
        default=20,
        ge=1,
        le=100,
    ),
    current_user: User = Depends(get_current_user),
    service: ProviderServiceOfferingService = Depends(
        get_provider_service_offering_service,
    ),
):
    return service.list_offerings(
        user_id=current_user.id,
        page=page,
        page_size=page_size,
    )


@router.post(
    "",
    response_model=ProviderServiceOfferingResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_service_offering(
    payload: ProviderServiceOfferingCreateRequest,
    current_user: User = Depends(get_current_user),
    service: ProviderServiceOfferingService = Depends(
        get_provider_service_offering_service,
    ),
):
    return service.create_offering(
        user_id=current_user.id,
        payload=payload,
    )


@router.get(
    "/{offering_id}",
    response_model=ProviderServiceOfferingResponse,
)
def get_service_offering(
    offering_id: UUID,
    current_user: User = Depends(get_current_user),
    service: ProviderServiceOfferingService = Depends(
        get_provider_service_offering_service,
    ),
):
    return service.get_offering(
        user_id=current_user.id,
        offering_id=offering_id,
    )


@router.patch(
    "/{offering_id}",
    response_model=ProviderServiceOfferingResponse,
)
def update_service_offering(
    offering_id: UUID,
    payload: ProviderServiceOfferingUpdateRequest,
    current_user: User = Depends(get_current_user),
    service: ProviderServiceOfferingService = Depends(
        get_provider_service_offering_service,
    ),
):
    return service.update_offering(
        user_id=current_user.id,
        offering_id=offering_id,
        payload=payload,
    )


@router.post(
    "/{offering_id}/activate",
    response_model=ProviderServiceOfferingResponse,
)
def activate_service_offering(
    offering_id: UUID,
    current_user: User = Depends(get_current_user),
    service: ProviderServiceOfferingService = Depends(
        get_provider_service_offering_service,
    ),
):
    return service.activate_offering(
        user_id=current_user.id,
        offering_id=offering_id,
    )


@router.post(
    "/{offering_id}/deactivate",
    response_model=ProviderServiceOfferingResponse,
)
def deactivate_service_offering(
    offering_id: UUID,
    current_user: User = Depends(get_current_user),
    service: ProviderServiceOfferingService = Depends(
        get_provider_service_offering_service,
    ),
):
    return service.deactivate_offering(
        user_id=current_user.id,
        offering_id=offering_id,
    )
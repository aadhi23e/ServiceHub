from typing import Annotated
import structlog

from fastapi import APIRouter, Depends, Query

from app.dependencies.provider import get_current_provider
from app.models.provider import ProviderProfile
from app.schemas.provider import (
    ProviderResponse,
    ProviderUpdateRequest,
)
from app.models.user import User

from app.services.provider_service import ProviderService

from app.dependencies.auth import get_current_user
from app.dependencies.core import DBSession
from app.schemas.service import (
    ServiceCreateRequest,
    ServiceListResponse,
    ServiceResponse,
    ServiceUpdateRequest,
)
from app.services.service_service import ServiceService

from app.schemas.availability import (
    AvailabilityCreateRequest,
    AvailabilityResponse,
    AvailabilityUpdateRequest,
)
from app.services.availability_service import AvailabilityService

router = APIRouter(
    prefix="/providers",
    tags=["providers"],
)

logger = structlog.get_logger("servicehub.provider")


@router.post(
    "/create",
    response_model=ProviderResponse,
)
def create_my_provider_profile(
    request: ProviderUpdateRequest,
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
    db: DBSession,
) -> ProviderProfile:

    provider_service = ProviderService(db)
    provider = provider_service.create_provider(
        request,
        user_id=current_user.id,
    )

    logger.info(
        "auth.register.success",
        user_id=provider.id,
        success=True,
    )
    return provider


@router.get(
    "/me",
    response_model=ProviderResponse,
)
def get_my_provider_profile(
    current_provider: Annotated[
        ProviderProfile,
        Depends(get_current_provider),
    ],
) -> ProviderProfile:
    return current_provider


@router.patch(
    "/me",
    response_model=ProviderResponse,
)
def update_my_provider_profile(
    request: ProviderUpdateRequest,
    current_provider: Annotated[
        ProviderProfile,
        Depends(get_current_provider),
    ],
    db: DBSession,
) -> ProviderProfile:
    provider_service = ProviderService(db)

    return provider_service.update_provider(
        current_provider,
        request,
    )


@router.get(
    "/me/services",
    response_model=ServiceListResponse,
)
def list_my_services(
    current_provider: Annotated[
        ProviderProfile,
        Depends(get_current_provider),
    ],
    db: DBSession,
    offset: int = Query(
        default=0,
        ge=0,
    ),
    limit: int = Query(
        default=50,
        ge=1,
        le=100,
    ),
) -> ServiceListResponse:
    service_service = ServiceService(db)

    items, total = service_service.list_services(
        current_provider,
        offset=offset,
        limit=limit,
    )

    return ServiceListResponse(
        items=items,
        total=total,
        offset=offset,
        limit=limit,
    )


@router.post(
    "/me/services",
    response_model=ServiceResponse,
    status_code=201,
)
def create_my_service(
    request: ServiceCreateRequest,
    current_provider: Annotated[
        ProviderProfile,
        Depends(get_current_provider),
    ],
    db: DBSession,
) -> ServiceResponse:
    service_service = ServiceService(db)

    return service_service.create_service(
        current_provider,
        request,
    )


@router.get(
    "/me/services/{service_id}",
    response_model=ServiceResponse,
)
def get_my_service(
    service_id: int,
    current_provider: Annotated[
        ProviderProfile,
        Depends(get_current_provider),
    ],
    db: DBSession,
) -> ServiceResponse:
    service_service = ServiceService(db)

    return service_service.get_service(
        current_provider,
        service_id,
    )


@router.patch(
    "/me/services/{service_id}",
    response_model=ServiceResponse,
)
def update_my_service(
    service_id: int,
    request: ServiceUpdateRequest,
    current_provider: Annotated[
        ProviderProfile,
        Depends(get_current_provider),
    ],
    db: DBSession,
) -> ServiceResponse:
    service_service = ServiceService(db)

    return service_service.update_service(
        current_provider,
        service_id,
        request,
    )


@router.post(
    "/me/services/{service_id}/activate",
    response_model=ServiceResponse,
)
def activate_my_service(
    service_id: int,
    current_provider: Annotated[
        ProviderProfile,
        Depends(get_current_provider),
    ],
    db: DBSession,
) -> ServiceResponse:
    service_service = ServiceService(db)

    return service_service.set_active(
        current_provider,
        service_id,
        is_active=True,
    )


@router.post(
    "/me/services/{service_id}/deactivate",
    response_model=ServiceResponse,
)
def deactivate_my_service(
    service_id: int,
    current_provider: Annotated[
        ProviderProfile,
        Depends(get_current_provider),
    ],
    db: DBSession,
) -> ServiceResponse:
    service_service = ServiceService(db)

    return service_service.set_active(
        current_provider,
        service_id,
        is_active=False,
    )


@router.get(
    "/me/availability",
    response_model=list[AvailabilityResponse],
)
def list_my_availability(
    current_provider: Annotated[
        ProviderProfile,
        Depends(get_current_provider),
    ],
    db: DBSession,
) -> list[AvailabilityResponse]:
    availability_service = AvailabilityService(db)

    return availability_service.list(current_provider)


@router.post(
    "/me/availability",
    response_model=AvailabilityResponse,
    status_code=201,
)
def create_my_availability(
    request: AvailabilityCreateRequest,
    current_provider: Annotated[
        ProviderProfile,
        Depends(get_current_provider),
    ],
    db: DBSession,
) -> AvailabilityResponse:
    availability_service = AvailabilityService(db)

    return availability_service.create(
        current_provider,
        request,
    )


@router.patch(
    "/me/availability/{availability_id}",
    response_model=AvailabilityResponse,
)
def update_my_availability(
    availability_id: int,
    request: AvailabilityUpdateRequest,
    current_provider: Annotated[
        ProviderProfile,
        Depends(get_current_provider),
    ],
    db: DBSession,
) -> AvailabilityResponse:
    availability_service = AvailabilityService(db)

    return availability_service.update(
        current_provider,
        availability_id,
        request,
    )


@router.post(
    "/me/availability/{availability_id}/activate",
    response_model=AvailabilityResponse,
)
def activate_my_availability(
    availability_id: int,
    current_provider: Annotated[
        ProviderProfile,
        Depends(get_current_provider),
    ],
    db: DBSession,
) -> AvailabilityResponse:
    availability_service = AvailabilityService(db)

    return availability_service.set_active(
        current_provider,
        availability_id,
        True,
    )


@router.post(
    "/me/availability/{availability_id}/deactivate",
    response_model=AvailabilityResponse,
)
def deactivate_my_availability(
    availability_id: int,
    current_provider: Annotated[
        ProviderProfile,
        Depends(get_current_provider),
    ],
    db: DBSession,
) -> AvailabilityResponse:
    availability_service = AvailabilityService(db)

    return availability_service.set_active(
        current_provider,
        availability_id,
        False,
    )


@router.delete(
    "/me/availability/{availability_id}",
    status_code=204,
)
def delete_my_availability(
    availability_id: int,
    current_provider: Annotated[
        ProviderProfile,
        Depends(get_current_provider),
    ],
    db: DBSession,
) -> None:
    availability_service = AvailabilityService(db)

    availability_service.delete(
        current_provider,
        availability_id,
    )

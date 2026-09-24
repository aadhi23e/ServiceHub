from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.dependencies.auth import get_current_user
from app.dependencies.authorization import (
    require_admin,
    require_customer,
    require_provider,
    require_provider_or_admin,
)
from app.dependencies.booking import BookingServiceDependency
from app.models.user import User
from app.schemas.booking import (
    BookingCreateRequest,
    BookingResponse,
)

router = APIRouter(
    prefix="/bookings",
    tags=["bookings"],
)


@router.post(
    "",
    response_model=BookingResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_booking(
    request: BookingCreateRequest,
    current_user: Annotated[
        User,
        Depends(require_customer),
    ],
    booking_service: BookingServiceDependency,
) -> BookingResponse:
    return booking_service.create_booking(
        customer=current_user,
        request=request,
    )


@router.get(
    "/my",
    response_model=list[BookingResponse],
)
def get_my_bookings(
    current_user: Annotated[
        User,
        Depends(require_customer),
    ],
    booking_service: BookingServiceDependency,
) -> list[BookingResponse]:
    return booking_service.get_customer_bookings(
        customer_id=current_user.id,
    )


@router.get(
    "/provider",
    response_model=list[BookingResponse],
)
def get_provider_bookings(
    current_user: Annotated[
        User,
        Depends(require_provider),
    ],
    booking_service: BookingServiceDependency,
) -> list[BookingResponse]:
    return booking_service.get_provider_bookings(
        provider_user_id=current_user.id,
    )


@router.get(
    "",
    response_model=list[BookingResponse],
)
def list_bookings(
    current_user: Annotated[
        User,
        Depends(require_admin),
    ],
    booking_service: BookingServiceDependency,
) -> list[BookingResponse]:
    return booking_service.list_all_bookings()


@router.get(
    "/{booking_id}",
    response_model=BookingResponse,
)
def get_booking(
    booking_id: int,
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
    booking_service: BookingServiceDependency,
) -> BookingResponse:
    return booking_service.get_booking_for_user(
        booking_id=booking_id,
        user=current_user,
    )


@router.post(
    "/{booking_id}/confirm",
    response_model=BookingResponse,
)
def confirm_booking(
    booking_id: int,
    current_user: Annotated[
        User,
        Depends(require_provider_or_admin),
    ],
    booking_service: BookingServiceDependency,
) -> BookingResponse:
    return booking_service.confirm_booking(
        booking_id=booking_id,
        user=current_user,
    )


@router.post(
    "/{booking_id}/reject",
    response_model=BookingResponse,
)
def reject_booking(
    booking_id: int,
    current_user: Annotated[
        User,
        Depends(require_provider_or_admin),
    ],
    booking_service: BookingServiceDependency,
) -> BookingResponse:
    return booking_service.reject_booking(
        booking_id=booking_id,
        user=current_user,
    )


@router.post(
    "/{booking_id}/start",
    response_model=BookingResponse,
)
def start_booking(
    booking_id: int,
    current_user: Annotated[
        User,
        Depends(require_provider_or_admin),
    ],
    booking_service: BookingServiceDependency,
) -> BookingResponse:
    return booking_service.start_booking(
        booking_id=booking_id,
        user=current_user,
    )


@router.post(
    "/{booking_id}/complete",
    response_model=BookingResponse,
)
def complete_booking(
    booking_id: int,
    current_user: Annotated[
        User,
        Depends(require_provider_or_admin),
    ],
    booking_service: BookingServiceDependency,
) -> BookingResponse:
    return booking_service.complete_booking(
        booking_id=booking_id,
        user=current_user,
    )


@router.post(
    "/{booking_id}/cancel",
    response_model=BookingResponse,
)
def cancel_booking(
    booking_id: int,
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
    booking_service: BookingServiceDependency,
) -> BookingResponse:
    return booking_service.cancel_booking(
        booking_id=booking_id,
        user=current_user,
    )

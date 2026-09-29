# backend/app/api/v1/user.py

from typing import Annotated
from uuid import UUID
from app.models.user import User

from fastapi import APIRouter, Depends, status

from app.dependencies.authorization import get_current_user
from app.dependencies.authorization import require_admin
from app.dependencies.core import DBSession
from app.models.user import User
from app.schemas.address import (
    AddressCreateRequest,
    AddressResponse,
    AddressUpdateRequest,
)
from app.schemas.user import UserResponse, UserUpdateRequest
from app.services.user_address_service import UserAddressService
from app.services.user_service import UserService

from app.repositories.user_repository import UserRepository

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

@router.get(
    "",
    response_model=list[UserResponse],
)
def list_users(
    current_user: Annotated[
        User,
        Depends(require_admin),
    ],
    db: DBSession,
) -> list[UserResponse]:
    user_repository = UserRepository(db)

    return user_repository.list_users()


@router.get(
    "/me",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
)
def get_current_user_profile(
    db: DBSession,
    current_user: User = Depends(get_current_user),
) -> UserResponse:
    """
    Return the authenticated user's profile.
    """

    service = UserService(db)

    user = service.get_current_user(
        user_id=current_user.id,
    )

    return UserResponse.model_validate(user)


@router.patch(
    "/me",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
)
def update_current_user_profile(
    data: UserUpdateRequest,
    db: DBSession,
    current_user: User = Depends(get_current_user),
) -> UserResponse:
    """
    Update the authenticated user's editable profile fields.
    """

    service = UserService(db)

    try:
        user = service.update_current_user(
            user_id=current_user.id,
            first_name=data.first_name,
            last_name=data.last_name,
            phone=data.phone,
        )

        db.commit()
        db.refresh(user)

    except Exception:
        db.rollback()
        raise

    return UserResponse.model_validate(user)


@router.get(
    "/me/addresses",
    response_model=list[AddressResponse],
    status_code=status.HTTP_200_OK,
)
def list_my_addresses(
    db: DBSession,
    current_user: User = Depends(get_current_user),
) -> list[AddressResponse]:
    """
    Return saved addresses belonging to the authenticated user.
    """

    service = UserAddressService(db)

    user_addresses = service.list_addresses(
        user_id=current_user.id,
    )

    return [
        AddressResponse(
            id=user_address.id,
            address_line_1=user_address.address.address_line_1,
            address_line_2=user_address.address.address_line_2,
            landmark=user_address.address.landmark,
            city=user_address.address.city,
            state=user_address.address.state,
            postal_code=user_address.address.postal_code,
            country_code=user_address.address.country_code,
            latitude=user_address.address.latitude,
            longitude=user_address.address.longitude,
            label=user_address.label,
            is_default=user_address.is_default,
            created_at=user_address.address.created_at,
            updated_at=user_address.address.updated_at,
        )
        for user_address in user_addresses
    ]


@router.post(
    "/me/addresses",
    response_model=AddressResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_my_address(
    data: AddressCreateRequest,
    db: DBSession,
    current_user: User = Depends(get_current_user),
) -> AddressResponse:
    """
    Create and save an address for the authenticated user.
    """

    service = UserAddressService(db)

    try:
        user_address = service.create_address(
            user_id=current_user.id,
            address_line_1=data.address_line_1,
            address_line_2=data.address_line_2,
            landmark=data.landmark,
            city=data.city,
            state=data.state,
            postal_code=data.postal_code,
            country_code=data.country_code,
            latitude=data.latitude,
            longitude=data.longitude,
            label=data.label,
            is_default=data.is_default,
        )

        db.commit()
        db.refresh(user_address)

    except Exception:
        db.rollback()
        raise

    address = user_address.address

    return AddressResponse(
        id=address.id,
        address_line_1=address.address_line_1,
        address_line_2=address.address_line_2,
        landmark=address.landmark,
        city=address.city,
        state=address.state,
        postal_code=address.postal_code,
        country_code=address.country_code,
        latitude=address.latitude,
        longitude=address.longitude,
        label=user_address.label,
        is_default=user_address.is_default,
        created_at=address.created_at,
        updated_at=address.updated_at,
    )


@router.patch(
    "/me/addresses/{user_address_id}",
    response_model=AddressResponse,
    status_code=status.HTTP_200_OK,
)
def update_my_address(
    user_address_id: UUID,
    data: AddressUpdateRequest,
    db: DBSession,
    current_user: User = Depends(get_current_user),
) -> AddressResponse:
    """
    Update a saved address owned by the authenticated user.
    """

    service = UserAddressService(db)

    try:
        user_address = service.update_address(
            user_id=current_user.id,
            user_address_id=user_address_id,
            address_line_1=data.address_line_1,
            address_line_2=data.address_line_2,
            landmark=data.landmark,
            city=data.city,
            state=data.state,
            postal_code=data.postal_code,
            country_code=data.country_code,
            latitude=data.latitude,
            longitude=data.longitude,
            label=data.label,
        )

        db.commit()
        db.refresh(user_address)

    except Exception:
        db.rollback()
        raise

    address = user_address.address

    return AddressResponse(
        id=address.id,
        address_line_1=address.address_line_1,
        address_line_2=address.address_line_2,
        landmark=address.landmark,
        city=address.city,
        state=address.state,
        postal_code=address.postal_code,
        country_code=address.country_code,
        latitude=address.latitude,
        longitude=address.longitude,
        label=user_address.label,
        is_default=user_address.is_default,
        created_at=address.created_at,
        updated_at=address.updated_at,
    )


@router.post(
    "/me/addresses/{user_address_id}/default",
    response_model=AddressResponse,
    status_code=status.HTTP_200_OK,
)
def set_my_default_address(
    user_address_id: UUID,
    db: DBSession,
    current_user: User = Depends(get_current_user),
) -> AddressResponse:
    """
    Make one of the authenticated user's saved addresses the default.
    """

    service = UserAddressService(db)

    try:
        user_address = service.set_default(
            user_id=current_user.id,
            user_address_id=user_address_id,
        )

        db.commit()
        db.refresh(user_address)

    except Exception:
        db.rollback()
        raise

    address = user_address.address

    return AddressResponse(
        id=address.id,
        address_line_1=address.address_line_1,
        address_line_2=address.address_line_2,
        landmark=address.landmark,
        city=address.city,
        state=address.state,
        postal_code=address.postal_code,
        country_code=address.country_code,
        latitude=address.latitude,
        longitude=address.longitude,
        label=user_address.label,
        is_default=user_address.is_default,
        created_at=address.created_at,
        updated_at=address.updated_at,
    )


@router.delete(
    "/me/addresses/{user_address_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_my_address(
    user_address_id: UUID,
    db: DBSession,
    current_user: User = Depends(get_current_user),
) -> None:
    """
    Delete a saved address belonging to the authenticated user.
    """

    service = UserAddressService(db)

    try:
        service.delete_address(
            user_id=current_user.id,
            user_address_id=user_address_id,
        )

        db.commit()

    except Exception:
        db.rollback()
        raise

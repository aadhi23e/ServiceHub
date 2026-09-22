from typing import Annotated

from fastapi import APIRouter, Depends

from app.core.exceptions import (
    AuthorizationError,
    ResourceNotFoundError,
)
from app.dependencies.auth import get_current_user
from app.dependencies.authorization import require_admin
from app.dependencies.core import DBSession
from app.enums.user import UserRole
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import (
    AdminUserUpdateRequest,
    UserResponse,
    UserUpdateRequest,
)


router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get(
    "/me",
    response_model=UserResponse,
)
def get_me(
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
) -> UserResponse:
    return current_user


@router.patch(
    "/me",
    response_model=UserResponse,
)
def update_me(
    request: UserUpdateRequest,
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
    db: DBSession,
) -> UserResponse:
    user_repository = UserRepository(db)

    return user_repository.update(
        current_user,
        first_name=request.first_name,
        last_name=request.last_name,
        phone=request.phone,
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
    "/{user_id}",
    response_model=UserResponse,
)
def get_user(
    user_id: int,
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
    db: DBSession,
) -> UserResponse:
    user_repository = UserRepository(db)

    # A non-admin user can only view their own account.
    if (
        current_user.role != UserRole.ADMIN.value
        and current_user.id != user_id
    ):
        raise AuthorizationError(
            message="You do not have permission to access this user.",
            code="USER_ACCESS_FORBIDDEN",
        )

    user = user_repository.get_by_id(user_id)

    if user is None:
        raise ResourceNotFoundError(
            message="User not found.",
            code="USER_NOT_FOUND",
        )

    return user


@router.patch(
    "/{user_id}",
    response_model=UserResponse,
)
def admin_update_user(
    user_id: int,
    request: AdminUserUpdateRequest,
    current_user: Annotated[
        User,
        Depends(require_admin),
    ],
    db: DBSession,
) -> UserResponse:
    user_repository = UserRepository(db)

    user = user_repository.get_by_id(user_id)

    if user is None:
        raise ResourceNotFoundError(
            message="User not found.",
            code="USER_NOT_FOUND",
        )

    return user_repository.update_admin_fields(
        user,
        first_name=request.first_name,
        last_name=request.last_name,
        phone=request.phone,
        role=request.role,
        status=request.status,
    )


@router.post(
    "/{user_id}/suspend",
    response_model=UserResponse,
)
def suspend_user(
    user_id: int,
    current_user: Annotated[
        User,
        Depends(require_admin),
    ],
    db: DBSession,
) -> UserResponse:
    user_repository = UserRepository(db)

    user = user_repository.get_by_id(user_id)

    if user is None:
        raise ResourceNotFoundError(
            message="User not found.",
            code="USER_NOT_FOUND",
        )

    return user_repository.suspend(user)


@router.post(
    "/{user_id}/activate",
    response_model=UserResponse,
)
def activate_user(
    user_id: int,
    current_user: Annotated[
        User,
        Depends(require_admin),
    ],
    db: DBSession,
) -> UserResponse:
    user_repository = UserRepository(db)

    user = user_repository.get_by_id(user_id)

    if user is None:
        raise ResourceNotFoundError(
            message="User not found.",
            code="USER_NOT_FOUND",
        )

    return user_repository.activate(user)
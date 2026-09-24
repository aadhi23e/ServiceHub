from typing import Annotated

import structlog
from fastapi import APIRouter, Depends, Response, status, Request

from app.dependencies.auth import get_auth_service
from app.services.auth_service import AuthService

from app.core.rate_limit_dependencies import (
    login_rate_limit,
    registration_rate_limit,
    refresh_rate_limit,
)
from app.dependencies.auth import get_auth_service
from app.schemas.auth import (
    LoginRequest,
    LoginResponse,
    RegisterRequest,
    RegisterResponse,
    TokenResponse,
    UserResponse,
)
from app.core.exceptions import AuthenticationError
from app.core.config import get_settings
from app.dependencies.auth import get_current_user
from app.models.user import User

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

logger = structlog.get_logger("servicehub.auth")


@router.post(
    "/login",
    response_model=LoginResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(login_rate_limit)],
)
def login(
    request: LoginRequest,
    response: Response,
    auth_service: Annotated[
        AuthService,
        Depends(get_auth_service),
    ],
) -> LoginResponse:
    login_response, refresh_token = auth_service.login(
        request,
    )

    settings = get_settings()

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        max_age=settings.refresh_token_expire_days * 24 * 60 * 60,
        httponly=True,
        secure=settings.environment == "production",
        samesite="lax",
        path="/api/v1/auth",
    )

    logger.info(
        "auth.login.success",
        user_id=login_response.user.id,
        success=True,
    )

    return login_response


@router.post(
    "/register",
    response_model=RegisterResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(registration_rate_limit)],
)
def register(
    request: RegisterRequest,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> RegisterResponse:
    user = auth_service.register(request)

    logger.info(
        "auth.register.success",
        user_id=user.id,
        success=True,
    )

    return RegisterResponse(user=user)


@router.post(
    "/logout",
    status_code=status.HTTP_204_NO_CONTENT,
)
def logout(
    request: Request,
    response: Response,
    auth_service: Annotated[
        AuthService,
        Depends(get_auth_service),
    ],
) -> None:
    refresh_token = request.cookies.get("refresh_token")

    auth_service.logout(refresh_token)

    settings = get_settings()

    response.delete_cookie(
        key="refresh_token",
        path="/api/v1/auth",
        secure=settings.environment == "production",
        httponly=True,
        samesite="lax",
    )

    logger.info(
        "auth.logout.success",
        success=True,
    )


@router.post(
    "/refresh",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(refresh_rate_limit)],
)
def refresh(
    request: Request,
    response: Response,
    auth_service: Annotated[
        AuthService,
        Depends(get_auth_service),
    ],
) -> TokenResponse:
    refresh_token = request.cookies.get(
        "refresh_token",
    )

    if not refresh_token:
        raise AuthenticationError(
            message="Refresh token is required.",
        )

    token_response, new_refresh_token = auth_service.refresh(
        refresh_token,
    )

    settings = get_settings()

    response.set_cookie(
        key="refresh_token",
        value=new_refresh_token,
        max_age=settings.refresh_token_expire_days * 24 * 60 * 60,
        httponly=True,
        secure=settings.environment == "production",
        samesite="lax",
        path="/api/v1/auth",
    )

    logger.info(
        "auth.refresh.success",
        success=True,
    )

    return token_response


@router.get(
    "/me",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
)
def get_me(
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
) -> UserResponse:
    return UserResponse.model_validate(
        current_user,
    )

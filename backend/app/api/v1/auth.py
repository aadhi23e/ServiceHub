from typing import Annotated

import structlog
from fastapi import APIRouter, Depends, status

from app.core.rate_limit_dependencies import registration_rate_limit
from app.dependencies.auth import get_auth_service
from app.schemas.auth import RegisterRequest, RegisterResponse
from app.services.auth_service import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

logger = structlog.get_logger("servicehub.auth")

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

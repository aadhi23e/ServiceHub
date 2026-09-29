from uuid import UUID

from fastapi import APIRouter, Depends, status, Query

from app.dependencies.authorization import require_admin
from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.dependencies.auth import get_current_user
from app.dependencies.core import DBSession
from app.enums.user import UserRole
from app.core.exceptions import AuthorizationError
from app.models.user import User
from app.schemas.provider_verification import (
    ProviderVerificationRejectRequest,
    ProviderVerificationResponse,
    ProviderVerificationListResponse
)
from app.services.provider_verification_service import (
    ProviderVerificationService,
)


router = APIRouter(
    prefix="/admin/provider-verifications",
    tags=["Admin Provider Verifications"],
)

# Return all provider verification requests waiting for admin review.
@router.get(
    "/pending",
    response_model=ProviderVerificationListResponse,
    status_code=status.HTTP_200_OK,
)
def list_pending_verifications(
    db: DBSession,
    admin: User = Depends(require_admin),
    search: str | None = Query(
        default=None,
        max_length=100,
    ),
    page: int = Query(
        default=1,
        ge=1,
    ),
    page_size: int = Query(
        default=20,
        ge=1,
        le=100,
    ),
) -> ProviderVerificationListResponse:

    service = ProviderVerificationService(db)

    (
        provider_verifications,
        total,
        total_pages,
    ) = service.list_pending(
        search=search,
        page=page,
        page_size=page_size,
    )

    return ProviderVerificationListResponse(
        items=provider_verifications,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
    )

# Return one provider verification request.
@router.get(
    "/{verification_id}",
    response_model=ProviderVerificationResponse,
    status_code=status.HTTP_200_OK,
)
def get_verification(
    verification_id: UUID,
    db: DBSession,
    admin: User = Depends(require_admin),
) -> ProviderVerificationResponse:
    service = ProviderVerificationService(db)

    return service.get(
        verification_id=verification_id,
    )

# Approve a pending provider verification.
@router.post(
    "/{verification_id}/approve",
    response_model=ProviderVerificationResponse,
    status_code=status.HTTP_200_OK,
)
def approve_provider_verification(
    verification_id: UUID,
    db: DBSession,
    current_user: User = Depends(get_current_user),
) -> ProviderVerificationResponse:
    if current_user.role != UserRole.ADMIN:
        raise AuthorizationError(
            message="Administrator access is required.",
        )

    service = ProviderVerificationService(db)

    try:
        verification = service.approve(
            verification_id=verification_id,
            admin_user=current_user,
        )

        db.commit()
        db.refresh(verification)

    except Exception:
        db.rollback()
        raise

    return ProviderVerificationResponse.model_validate(
        verification,
    )


# Reject a pending provider verification.
@router.post(
    "/{verification_id}/reject",
    response_model=ProviderVerificationResponse,
    status_code=status.HTTP_200_OK,
)
def reject_provider_verification(
    verification_id: UUID,
    data: ProviderVerificationRejectRequest,
    db: DBSession,
    current_user: User = Depends(get_current_user),
) -> ProviderVerificationResponse:
    if current_user.role != UserRole.ADMIN:
        raise AuthorizationError(
            message="Administrator access is required.",
        )

    service = ProviderVerificationService(db)

    try:
        verification = service.reject(
            verification_id=verification_id,
            admin_user=current_user,
            reason=data.reason,
        )

        db.commit()
        db.refresh(verification)

    except Exception:
        db.rollback()
        raise

    return ProviderVerificationResponse.model_validate(
        verification,
    )
from datetime import datetime, timezone
from uuid import UUID
from math import ceil

from sqlalchemy.orm import Session

from app.enums.provider import ProviderStatus
from app.enums.servicehub import VerificationStatus
from app.core.exceptions import ConflictError
from app.core.exceptions import ResourceNotFoundError
from app.models.provider_verification import ProviderVerification
from app.models.user import User
from app.repositories.audit_log_repository import AuditLogRepository
from app.repositories.provider_organization_repository import (
    ProviderOrganizationRepository,
)
from app.repositories.provider_verification_repository import (
    ProviderVerificationRepository,
)


class ProviderVerificationService:
    def __init__(self, db: Session):
        self.db = db

        self.verification_repository = (
            ProviderVerificationRepository(db)
        )

        self.organization_repository = (
            ProviderOrganizationRepository(db)
        )

        self.audit_repository = AuditLogRepository(db)

    # Return public organizations.
    def list_pending(
        self,
        *,
        search: str | None,
        page: int,
        page_size: int,
    ) -> tuple[list[ProviderVerification], int, int]:

        offset = (page - 1) * page_size

        provider_verifications, total = (
            self.verification_repository.list_pending(
                search=search,
                offset=offset,
                limit=page_size,
            )
        )

        total_pages = ceil(total / page_size) if total else 0

        return provider_verifications, total, total_pages

    # Approve a pending provider verification and activate its organization.
    def approve(
        self,
        *,
        verification_id: UUID,
        admin_user: User,
    ) -> ProviderVerification:
        verification = (
            self.verification_repository.get_by_id(
                verification_id,
            )
        )

        if verification is None:
            raise ResourceNotFoundError(
                message="Provider verification not found.",
            )

        if verification.status != VerificationStatus.PENDING:
            raise ConflictError(
                code="INVALID_VERIFICATION_STATUS",
                message=(
                    "Only pending provider verifications "
                    "can be approved."
                ),
            )

        organization = (
            self.organization_repository.get_by_id(
                verification.organization_id,
            )
        )

        if organization is None:
            raise ResourceNotFoundError(
                message=(
                    "The organization associated with "
                    "this provider verification was not found."
                ),
            )

        if organization.status != ProviderStatus.PENDING:
            raise ConflictError(
                code="INVALID_ORGANIZATION_STATUS",
                message=(
                    "Only pending provider organizations "
                    "can be activated through verification."
                ),
            )

        now = datetime.now(timezone.utc)

        verification.status = VerificationStatus.APPROVED
        verification.reviewed_by = admin_user.id
        verification.reviewed_at = now
        verification.rejection_reason = None

        organization.status = ProviderStatus.ACTIVE

        self.db.flush()

        self.audit_repository.create(
            actor_user_id=admin_user.id,
            action="PROVIDER_VERIFICATION_APPROVED",
            entity_type="PROVIDER_VERIFICATION",
            entity_id=verification.id,
            metadata={
                "organization_id": str(
                    organization.id,
                ),
                "verification_status": (
                    VerificationStatus.APPROVED.value
                ),
                "organization_status": (
                    ProviderStatus.ACTIVE.value
                ),
            },
        )

        return verification

    # Reject a pending provider verification and keep its organization pending.
    def reject(
        self,
        *,
        verification_id: UUID,
        admin_user: User,
        reason: str,
    ) -> ProviderVerification:
        verification = (
            self.verification_repository.get_by_id(
                verification_id,
            )
        )

        if verification is None:
            raise ResourceNotFoundError(
                message="Provider verification not found.",
            )

        if verification.status != VerificationStatus.PENDING:
            raise ConflictError(
                code="INVALID_VERIFICATION_STATUS",
                message=(
                    "Only pending provider verifications "
                    "can be rejected."
                ),
            )

        organization = (
            self.organization_repository.get_by_id(
                verification.organization_id,
            )
        )

        if organization is None:
            raise ResourceNotFoundError(
                message=(
                    "The organization associated with "
                    "this provider verification was not found."
                ),
            )

        if organization.status != ProviderStatus.PENDING:
            raise ConflictError(
                code="INVALID_ORGANIZATION_STATUS",
                message=(
                    "Only pending provider organizations "
                    "can have their initial verification rejected."
                ),
            )

        cleaned_reason = reason.strip()

        if not cleaned_reason:
            raise ConflictError(
                code="INVALID_REJECTION_REASON",
                message="A rejection reason is required.",
            )

        now = datetime.now(timezone.utc)

        verification.status = VerificationStatus.REJECTED
        verification.reviewed_by = admin_user.id
        verification.reviewed_at = now
        verification.rejection_reason = cleaned_reason

        # The organization intentionally remains PENDING.
        self.db.flush()

        self.audit_repository.create(
            actor_user_id=admin_user.id,
            action="PROVIDER_VERIFICATION_REJECTED",
            entity_type="PROVIDER_VERIFICATION",
            entity_id=verification.id,
            metadata={
                "organization_id": str(
                    organization.id,
                ),
                "verification_status": (
                    VerificationStatus.REJECTED.value
                ),
                "organization_status": (
                    organization.status.value
                ),
                "rejection_reason": cleaned_reason,
            },
        )

        return verification
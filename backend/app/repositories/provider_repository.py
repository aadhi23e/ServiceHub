from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.provider_verification import ProviderVerification
from app.enums.servicehub import VerificationStatus

class ProviderVerificationRepository:
    def __init__(self, db: Session):
        self.db = db

    # Return a provider verification by ID.
    def get_by_id(
        self,
        verification_id: UUID,
    ) -> ProviderVerification | None:
        statement = (
            select(ProviderVerification)
            .where(
                ProviderVerification.id == verification_id,
            )
        )

        return self.db.scalar(statement)

    # Return the pending verification for an organization.
    def get_pending_by_organization_id(
        self,
        organization_id: UUID,
    ) -> ProviderVerification | None:
        statement = (
            select(ProviderVerification)
            .where(
                ProviderVerification.organization_id
                == organization_id,
                ProviderVerification.status
                == VerificationStatus.PENDING,
            )
            .order_by(
                ProviderVerification.created_at.desc(),
            )
            .limit(1)
        )

        return self.db.scalar(statement)

    # Save verification changes without committing.
    def flush(
        self,
        verification: ProviderVerification,
    ) -> ProviderVerification:
        self.db.flush()

        return verification
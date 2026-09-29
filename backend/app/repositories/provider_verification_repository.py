from uuid import UUID

from sqlalchemy import select, func, or_
from sqlalchemy.orm import Session

from app.models.provider_verification import ProviderVerification
from app.enums.provider import VerificationStatus
from app.models import ProviderOrganization

class ProviderVerificationRepository:
    def __init__(self, db: Session):
        self.db = db
        
    def list_pending(
        self,
        *,
        offset: int = 0,
        limit: int = 50,
        search: str | None = None,
    ) -> tuple[list[ProviderVerification], int]:

        conditions = [
            ProviderVerification.status == VerificationStatus.PENDING,
        ]

        if search:
            search_pattern = f"%{search.strip()}%"

            conditions.append(
                or_(
                    ProviderOrganization.name.ilike(search_pattern),
                    ProviderOrganization.legal_name.ilike(search_pattern),
                )
            )

        count_statement = (
            select(func.count(ProviderVerification.id))
            .join(
                ProviderOrganization,
                ProviderOrganization.id
                == ProviderVerification.organization_id,
            )
            .where(*conditions)
        )

        total = int(self.db.scalar(count_statement) or 0)

        statement = (
            select(ProviderVerification)
            .join(
                ProviderOrganization,
                ProviderOrganization.id
                == ProviderVerification.organization_id,
            )
            .where(*conditions)
            .order_by(
                ProviderVerification.created_at.asc(),
                ProviderVerification.id.asc(),
            )
            .offset(offset)
            .limit(limit)
        )

        verifications = list(self.db.scalars(statement).all())

        return verifications, total

    # Get a provider verification by ID.
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

    # Save verification changes without committing the transaction.
    def flush(
        self,
        verification: ProviderVerification,
    ) -> ProviderVerification:
        self.db.flush()
        return verification
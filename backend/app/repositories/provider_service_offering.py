from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from app.models.provider_service_offering import ProviderServiceOffering


class ProviderServiceOfferingRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(
        self,
        *,
        offering_id: UUID,
        organization_id: UUID,
    ) -> ProviderServiceOffering | None:
        stmt = (
            select(ProviderServiceOffering)
            .options(
                selectinload(
                    ProviderServiceOffering.service,
                )
            )
            .where(
                ProviderServiceOffering.id == offering_id,
                ProviderServiceOffering.organization_id
                == organization_id,
            )
        )

        return self.db.scalar(stmt)

    def get_by_service(
        self,
        *,
        organization_id: UUID,
        service_id: UUID,
    ) -> ProviderServiceOffering | None:
        stmt = select(ProviderServiceOffering).where(
            ProviderServiceOffering.organization_id == organization_id,
            ProviderServiceOffering.service_id == service_id,
        )

        return self.db.scalar(stmt)

    def list(
        self,
        *,
        organization_id: UUID,
        page: int,
        page_size: int,
    ) -> tuple[list[ProviderServiceOffering], int]:
        offset = (page - 1) * page_size

        total_stmt = (
            select(func.count())
            .select_from(ProviderServiceOffering)
            .where(
                ProviderServiceOffering.organization_id
                == organization_id,
            )
        )

        total = self.db.scalar(total_stmt) or 0

        stmt = (
            select(ProviderServiceOffering)
            .options(
                selectinload(
                    ProviderServiceOffering.service,
                )
            )
            .where(
                ProviderServiceOffering.organization_id
                == organization_id,
            )
            .order_by(
                ProviderServiceOffering.created_at.desc()
            )
            .offset(offset)
            .limit(page_size)
        )

        items = list(self.db.scalars(stmt).all())

        return items, total

    def create(
        self,
        offering: ProviderServiceOffering,
    ) -> ProviderServiceOffering:
        self.db.add(offering)
        self.db.flush()
        self.db.refresh(offering)

        return offering
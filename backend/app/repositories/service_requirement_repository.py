from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.service_requirement import ServiceRequirement


class ServiceRequirementRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(
        self,
        requirement_id: UUID,
    ) -> ServiceRequirement | None:
        statement = select(ServiceRequirement).where(
            ServiceRequirement.id == requirement_id,
        )

        return self.db.scalar(statement)

    def get_for_service(
        self,
        *,
        service_id: UUID,
        requirement_id: UUID,
    ) -> ServiceRequirement | None:
        statement = select(ServiceRequirement).where(
            ServiceRequirement.id == requirement_id,
            ServiceRequirement.service_id == service_id,
        )

        return self.db.scalar(statement)

    def get_by_key(
        self,
        *,
        service_id: UUID,
        key: str,
    ) -> ServiceRequirement | None:
        statement = select(ServiceRequirement).where(
            ServiceRequirement.service_id == service_id,
            ServiceRequirement.key == key,
        )

        return self.db.scalar(statement)

    def list_for_service(
        self,
        *,
        service_id: UUID,
        active_only: bool = False,
    ) -> list[ServiceRequirement]:
        statement = select(ServiceRequirement).where(
            ServiceRequirement.service_id == service_id,
        )

        if active_only:
            statement = statement.where(
                ServiceRequirement.is_active.is_(True),
            )

        statement = statement.order_by(
            ServiceRequirement.sort_order.asc(),
            ServiceRequirement.created_at.asc(),
        )

        return list(self.db.scalars(statement).all())

    def create(
        self,
        requirement: ServiceRequirement,
    ) -> ServiceRequirement:
        self.db.add(requirement)
        self.db.flush()

        return requirement

    def update(
        self,
        requirement: ServiceRequirement,
    ) -> ServiceRequirement:
        self.db.flush()

        return requirement
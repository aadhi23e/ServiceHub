from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.service import Service


class ServiceRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(
        self,
        service_id: UUID,
    ) -> Service | None:
        statement = select(Service).where(
            Service.id == service_id,
        )

        return self.db.scalar(statement)

    def get_by_slug(
        self,
        slug: str,
    ) -> Service | None:
        statement = select(Service).where(
            Service.slug == slug,
        )

        return self.db.scalar(statement)

    def list_all(
        self,
        *,
        active_only: bool = False,
        category_id: UUID | None = None,
    ) -> list[Service]:
        statement = select(Service)

        if active_only:
            statement = statement.where(
                Service.is_active.is_(True),
            )

        if category_id is not None:
            statement = statement.where(
                Service.category_id == category_id,
            )

        statement = statement.order_by(
            Service.name.asc(),
        )

        return list(self.db.scalars(statement).all())

    def create(
        self,
        service: Service,
    ) -> Service:
        self.db.add(service)
        self.db.flush()

        return service

    def update(
        self,
        service: Service,
    ) -> Service:
        self.db.flush()

        return service
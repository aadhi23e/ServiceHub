from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.service import Service


class ServiceRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(
        self,
        service_id: int,
    ) -> Service | None:
        statement = select(Service).where(Service.id == service_id)

        return self.db.scalar(statement)

    def get_by_id_for_provider(
        self,
        service_id: int,
        provider_id: int,
    ) -> Service | None:
        statement = select(Service).where(
            Service.id == service_id,
            Service.provider_id == provider_id,
        )

        return self.db.scalar(statement)

    def list_by_provider(
        self,
        provider_id: int,
        *,
        offset: int = 0,
        limit: int = 50,
    ) -> tuple[list[Service], int]:
        statement = (
            select(Service)
            .where(Service.provider_id == provider_id)
            .order_by(Service.id)
            .offset(offset)
            .limit(limit)
        )

        items = list(self.db.scalars(statement).all())

        count_statement = (
            select(func.count())
            .select_from(Service)
            .where(Service.provider_id == provider_id)
        )

        total = self.db.scalar(count_statement) or 0

        return items, total

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
        *,
        category_id: int | None = None,
        name: str | None = None,
        description: str | None = None,
        duration_minutes: int | None = None,
        price=None,
    ) -> Service:
        if category_id is not None:
            service.category_id = category_id

        if name is not None:
            service.name = name

        if description is not None:
            service.description = description

        if duration_minutes is not None:
            service.duration_minutes = duration_minutes

        if price is not None:
            service.price = price

        self.db.flush()

        return service

    def set_active(
        self,
        service: Service,
        is_active: bool,
    ) -> Service:
        service.is_active = is_active
        self.db.flush()

        return service

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.service_category import ServiceCategory


class ServiceCategoryRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(
        self,
        category_id: UUID,
    ) -> ServiceCategory | None:
        statement = select(ServiceCategory).where(
            ServiceCategory.id == category_id,
        )

        return self.db.scalar(statement)

    def get_by_slug(
        self,
        slug: str,
    ) -> ServiceCategory | None:
        statement = select(ServiceCategory).where(
            ServiceCategory.slug == slug,
        )

        return self.db.scalar(statement)

    def list_all(
        self,
        *,
        active_only: bool = False,
    ) -> list[ServiceCategory]:
        statement = select(ServiceCategory)

        if active_only:
            statement = statement.where(
                ServiceCategory.is_active.is_(True),
            )

        statement = statement.order_by(
            ServiceCategory.name.asc(),
        )

        return list(self.db.scalars(statement).all())

    def create(
        self,
        category: ServiceCategory,
    ) -> ServiceCategory:
        self.db.add(category)
        self.db.flush()

        return category

    def update(
        self,
        category: ServiceCategory,
    ) -> ServiceCategory:
        self.db.flush()

        return category
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.service_category import ServiceCategory


class ServiceCategoryRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(
        self,
        category_id: int,
    ) -> ServiceCategory | None:
        statement = select(ServiceCategory).where(ServiceCategory.id == category_id)

        return self.db.scalar(statement)

    def list_active(self) -> list[ServiceCategory]:
        statement = (
            select(ServiceCategory)
            .where(ServiceCategory.is_active.is_(True))
            .order_by(ServiceCategory.name)
        )

        return list(self.db.scalars(statement).all())

    def create(self, category: ServiceCategory) -> ServiceCategory:

        self.db.add(category)
        self.db.flush()
        self.db.commit()
        self.db.refresh(category)  # TODO
        return category

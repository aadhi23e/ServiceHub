from uuid import UUID

from sqlalchemy import func, or_, select
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

    def get_active_by_id(
        self,
        category_id: UUID,
    ) -> ServiceCategory | None:
        statement = select(ServiceCategory).where(
            ServiceCategory.id == category_id,
            ServiceCategory.is_active.is_(True),
        )

        return self.db.scalar(statement)

    def parent_exists(
        self,
        parent_id: UUID,
    ) -> bool:
        statement = select(
            func.count(ServiceCategory.id)
        ).where(
            ServiceCategory.id == parent_id,
            ServiceCategory.is_active.is_(True),
        )

        return bool(self.db.scalar(statement))

    def create(
        self,
        *,
        name: str,
        description: str | None,
        parent_id: UUID | None,
    ) -> ServiceCategory:

        category = ServiceCategory(
            name=name,
            description=description,
            parent_id=parent_id,
            is_active=True,
        )

        self.db.add(category)
        self.db.flush()

        return category

    def update(
        self,
        category: ServiceCategory,
        *,
        name: str | None = None,
        description: str | None = None,
        parent_id: UUID | None = None,
    ) -> ServiceCategory:

        if name is not None:
            category.name = name

        if description is not None:
            category.description = description

        if parent_id is not None:
            category.parent_id = parent_id

        self.db.flush()

        return category

    def list_active(
        self,
        *,
        search: str | None,
        parent_id: UUID | None,
        page: int,
        page_size: int,
    ) -> tuple[list[ServiceCategory], int]:

        conditions = [
            ServiceCategory.is_active.is_(True),
        ]

        if search:
            pattern = f"%{search.strip()}%"

            conditions.append(
                or_(
                    ServiceCategory.name.ilike(pattern),
                    ServiceCategory.description.ilike(pattern),
                )
            )

        if parent_id is not None:
            conditions.append(
                ServiceCategory.parent_id == parent_id
            )

        count_statement = (
            select(func.count())
            .select_from(ServiceCategory)
            .where(*conditions)
        )

        total = int(
            self.db.scalar(count_statement) or 0
        )

        offset = (page - 1) * page_size

        statement = (
            select(ServiceCategory)
            .where(*conditions)
            .order_by(
                ServiceCategory.name.asc(),
            )
            .offset(offset)
            .limit(page_size)
        )

        categories = list(
            self.db.scalars(statement).all()
        )

        return categories, total
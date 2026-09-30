from uuid import UUID, uuid4

from app.core.exceptions import ResourceConflictError
from app.core.exceptions import ResourceNotFoundError
from app.models.service_category import ServiceCategory
from app.repositories.service_category_repository import (
    ServiceCategoryRepository,
)


class ServiceCategoryService:
    def __init__(self, db):
        self.repository = ServiceCategoryRepository(db)

    def list_categories(
        self,
        *,
        active_only: bool = False,
    ) -> list[ServiceCategory]:
        return self.repository.list_all(
            active_only=active_only,
        )

    def get_category(
        self,
        *,
        category_id: UUID,
    ) -> ServiceCategory:
        category = self.repository.get_by_id(category_id)

        if category is None:
            raise ResourceNotFoundError(
                message="Service category not found.",
            )

        return category

    def create_category(
        self,
        *,
        name: str,
        slug: str,
        description: str | None,
    ) -> ServiceCategory:
        normalized_slug = slug.strip().lower()

        existing = self.repository.get_by_slug(normalized_slug)

        if existing is not None:
            raise ResourceConflictError(
                message="A service category with this slug already exists.",
            )

        category = ServiceCategory(
            id=uuid4(),
            name=name.strip(),
            slug=normalized_slug,
            description=description.strip()
            if description is not None
            else None,
            is_active=True,
        )

        return self.repository.create(category)

    def update_category(
        self,
        *,
        category_id: UUID,
        name: str | None,
        slug: str | None,
        description: str | None,
    ) -> ServiceCategory:
        category = self.get_category(
            category_id=category_id,
        )

        if slug is not None:
            normalized_slug = slug.strip().lower()

            existing = self.repository.get_by_slug(
                normalized_slug,
            )

            if existing is not None and existing.id != category.id:
                raise ResourceConflictError(
                    message="A service category with this slug already exists.",
                )

            category.slug = normalized_slug

        if name is not None:
            category.name = name.strip()

        if description is not None:
            category.description = description.strip()

        return self.repository.update(category)

    def activate_category(
        self,
        *,
        category_id: UUID,
    ) -> ServiceCategory:
        category = self.get_category(
            category_id=category_id,
        )

        category.is_active = True

        return self.repository.update(category)

    def deactivate_category(
        self,
        *,
        category_id: UUID,
    ) -> ServiceCategory:
        category = self.get_category(
            category_id=category_id,
        )

        category.is_active = False

        return self.repository.update(category)
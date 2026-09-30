from uuid import UUID, uuid4

from app.core.exceptions import ResourceConflictError
from app.core.exceptions import ResourceNotFoundError
from app.models.service import Service
from app.repositories.service_category_repository import (
    ServiceCategoryRepository,
)
from app.repositories.service_repository import ServiceRepository


class ServiceService:
    def __init__(self, db):
        self.repository = ServiceRepository(db)
        self.category_repository = ServiceCategoryRepository(db)

    def list_services(
        self,
        *,
        active_only: bool = False,
        category_id: UUID | None = None,
    ) -> list[Service]:
        return self.repository.list_all(
            active_only=active_only,
            category_id=category_id,
        )

    def get_service(
        self,
        *,
        service_id: UUID,
    ) -> Service:
        service = self.repository.get_by_id(service_id)

        if service is None:
            raise ResourceNotFoundError(
                message="Service not found.",
            )

        return service

    def create_service(
        self,
        *,
        category_id: UUID,
        name: str,
        slug: str,
        description: str | None,
    ) -> Service:
        category = self.category_repository.get_by_id(
            category_id,
        )

        if category is None:
            raise ResourceNotFoundError(
                message="Service category not found.",
            )

        if not category.is_active:
            raise ResourceConflictError(
                message="Cannot create a service under an inactive category.",
            )

        normalized_slug = slug.strip().lower()

        existing = self.repository.get_by_slug(
            normalized_slug,
        )

        if existing is not None:
            raise ResourceConflictError(
                message="A service with this slug already exists.",
            )

        service = Service(
            id=uuid4(),
            category_id=category_id,
            name=name.strip(),
            slug=normalized_slug,
            description=description.strip()
            if description is not None
            else None,
            is_active=True,
        )

        return self.repository.create(service)

    def update_service(
        self,
        *,
        service_id: UUID,
        category_id: UUID | None,
        name: str | None,
        slug: str | None,
        description: str | None,
    ) -> Service:
        service = self.get_service(
            service_id=service_id,
        )

        if category_id is not None:
            category = self.category_repository.get_by_id(
                category_id,
            )

            if category is None:
                raise ResourceNotFoundError(
                    message="Service category not found.",
                )

            if not category.is_active:
                raise ResourceConflictError(
                    message="Cannot move a service to an inactive category.",
                )

            service.category_id = category_id

        if slug is not None:
            normalized_slug = slug.strip().lower()

            existing = self.repository.get_by_slug(
                normalized_slug,
            )

            if existing is not None and existing.id != service.id:
                raise ResourceConflictError(
                    message="A service with this slug already exists.",
                )

            service.slug = normalized_slug

        if name is not None:
            service.name = name.strip()

        if description is not None:
            service.description = description.strip()

        return self.repository.update(service)

    def activate_service(
        self,
        *,
        service_id: UUID,
    ) -> Service:
        service = self.get_service(
            service_id=service_id,
        )

        category = self.category_repository.get_by_id(
            service.category_id,
        )

        if category is None:
            raise ResourceNotFoundError(
                message="Service category not found.",
            )

        if not category.is_active:
            raise ResourceConflictError(
                message="Cannot activate a service under an inactive category.",
            )

        service.is_active = True

        return self.repository.update(service)

    def deactivate_service(
        self,
        *,
        service_id: UUID,
    ) -> Service:
        service = self.get_service(
            service_id=service_id,
        )

        service.is_active = False

        return self.repository.update(service)
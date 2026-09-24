from sqlalchemy.orm import Session

from app.core.exceptions import (
    ConflictError,
    ResourceNotFoundError,
)
from app.models.provider import ProviderProfile
from app.models.service import Service
from app.repositories.service_category_repository import (
    ServiceCategoryRepository,
)
from app.repositories.service_repository import ServiceRepository
from app.schemas.service import (
    ServiceCreateRequest,
    ServiceUpdateRequest,
)


class ServiceService:
    def __init__(self, db: Session) -> None:
        self.db = db

        self.service_repository = ServiceRepository(db)
        self.category_repository = ServiceCategoryRepository(db)

    def list_services(
        self,
        provider: ProviderProfile,
        *,
        offset: int,
        limit: int,
    ) -> tuple[list[Service], int]:
        return self.service_repository.list_by_provider(
            provider.id,
            offset=offset,
            limit=limit,
        )

    def get_service(
        self,
        provider: ProviderProfile,
        service_id: int,
    ) -> Service:
        service = self.service_repository.get_by_id_for_provider(
            service_id,
            provider.id,
        )

        if service is None:
            raise ResourceNotFoundError(
                message="Service not found.",
                code="SERVICE_NOT_FOUND",
            )

        return service

    def create_service(
        self,
        provider: ProviderProfile,
        request: ServiceCreateRequest,
    ) -> Service:
        category = self.category_repository.get_by_id(request.category_id)

        if category is None:
            raise ResourceNotFoundError(
                message="Service category not found.",
                code="SERVICE_CATEGORY_NOT_FOUND",
            )

        if not category.is_active:
            raise ConflictError(
                message="The selected service category is inactive.",
                code="SERVICE_CATEGORY_INACTIVE",
            )

        service = Service(
            provider_id=provider.id,
            category_id=request.category_id,
            name=request.name.strip(),
            description=request.description,
            duration_minutes=request.duration_minutes,
            price=request.price,
            is_active=True,
        )

        self.service_repository.create(service)

        self.db.commit()
        self.db.refresh(service)

        return service

    def update_service(
        self,
        provider: ProviderProfile,
        service_id: int,
        request: ServiceUpdateRequest,
    ) -> Service:
        service = self.get_service(
            provider,
            service_id,
        )

        if request.category_id is not None:
            category = self.category_repository.get_by_id(request.category_id)

            if category is None:
                raise ResourceNotFoundError(
                    message="Service category not found.",
                    code="SERVICE_CATEGORY_NOT_FOUND",
                )

            if not category.is_active:
                raise ConflictError(
                    message="The selected service category is inactive.",
                    code="SERVICE_CATEGORY_INACTIVE",
                )

        updated_service = self.service_repository.update(
            service,
            category_id=request.category_id,
            name=request.name.strip() if request.name is not None else None,
            description=request.description,
            duration_minutes=request.duration_minutes,
            price=request.price,
        )

        self.db.commit()
        self.db.refresh(updated_service)

        return updated_service

    def set_active(
        self,
        provider: ProviderProfile,
        service_id: int,
        *,
        is_active: bool,
    ) -> Service:
        service = self.get_service(
            provider,
            service_id,
        )

        if service.is_active == is_active:
            return service

        self.service_repository.set_active(
            service,
            is_active,
        )

        self.db.commit()
        self.db.refresh(service)

        return service

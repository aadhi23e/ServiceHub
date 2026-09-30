from uuid import UUID, uuid4

from app.core.exceptions import ResourceConflictError
from app.core.exceptions import ResourceNotFoundError
from app.models.service_requirement import ServiceRequirement
from app.repositories.service_repository import ServiceRepository
from app.repositories.service_requirement_repository import (
    ServiceRequirementRepository,
)


class ServiceRequirementService:
    def __init__(self, db):
        self.repository = ServiceRequirementRepository(db)
        self.service_repository = ServiceRepository(db)

    def list_requirements(
        self,
        *,
        service_id: UUID,
        active_only: bool = False,
    ) -> list[ServiceRequirement]:
        self._get_service(service_id)

        return self.repository.list_for_service(
            service_id=service_id,
            active_only=active_only,
        )

    def get_requirement(
        self,
        *,
        service_id: UUID,
        requirement_id: UUID,
    ) -> ServiceRequirement:
        self._get_service(service_id)

        requirement = self.repository.get_for_service(
            service_id=service_id,
            requirement_id=requirement_id,
        )

        if requirement is None:
            raise ResourceNotFoundError(
                message="Service requirement not found.",
            )

        return requirement

    def create_requirement(
        self,
        *,
        service_id: UUID,
        key: str,
        label: str,
        description: str | None,
        requirement_type,
        is_required: bool,
        sort_order: int,
    ) -> ServiceRequirement:
        self._get_service(service_id)

        normalized_key = key.strip().lower()

        existing = self.repository.get_by_key(
            service_id=service_id,
            key=normalized_key,
        )

        if existing is not None:
            raise ResourceConflictError(
                message="A requirement with this key already exists for this service.",
            )

        requirement = ServiceRequirement(
            id=uuid4(),
            service_id=service_id,
            key=normalized_key,
            label=label.strip(),
            description=description.strip()
            if description is not None
            else None,
            requirement_type=requirement_type,
            is_required=is_required,
            sort_order=sort_order,
            is_active=True,
        )

        return self.repository.create(requirement)

    def update_requirement(
        self,
        *,
        service_id: UUID,
        requirement_id: UUID,
        key: str | None,
        label: str | None,
        description: str | None,
        requirement_type,
        is_required: bool | None,
        sort_order: int | None,
    ) -> ServiceRequirement:
        requirement = self.get_requirement(
            service_id=service_id,
            requirement_id=requirement_id,
        )

        if key is not None:
            normalized_key = key.strip().lower()

            existing = self.repository.get_by_key(
                service_id=service_id,
                key=normalized_key,
            )

            if (
                existing is not None
                and existing.id != requirement.id
            ):
                raise ResourceConflictError(
                    message="A requirement with this key already exists for this service.",
                )

            requirement.key = normalized_key

        if label is not None:
            requirement.label = label.strip()

        if description is not None:
            requirement.description = description.strip()

        if requirement_type is not None:
            requirement.requirement_type = requirement_type

        if is_required is not None:
            requirement.is_required = is_required

        if sort_order is not None:
            requirement.sort_order = sort_order

        return self.repository.update(requirement)

    def activate_requirement(
        self,
        *,
        service_id: UUID,
        requirement_id: UUID,
    ) -> ServiceRequirement:
        requirement = self.get_requirement(
            service_id=service_id,
            requirement_id=requirement_id,
        )

        requirement.is_active = True

        return self.repository.update(requirement)

    def deactivate_requirement(
        self,
        *,
        service_id: UUID,
        requirement_id: UUID,
    ) -> ServiceRequirement:
        requirement = self.get_requirement(
            service_id=service_id,
            requirement_id=requirement_id,
        )

        requirement.is_active = False

        return self.repository.update(requirement)

    def _get_service(
        self,
        service_id: UUID,
    ):
        service = self.service_repository.get_by_id(service_id)

        if service is None:
            raise ResourceNotFoundError(
                message="Service not found.",
            )

        return service
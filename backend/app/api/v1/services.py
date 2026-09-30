from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status

from app.dependencies.authorization import get_current_user, require_admin
from app.dependencies.core import DBSession
from app.models.user import User
from app.schemas.service import (
    ServiceCreateRequest,
    ServiceResponse,
    ServiceUpdateRequest,
)
from app.schemas.service_requirement import (
    ServiceRequirementCreateRequest,
    ServiceRequirementResponse,
    ServiceRequirementUpdateRequest,
)
from app.services.service_requirement_service import (
    ServiceRequirementService,
)
from app.services.service_service import ServiceService


router = APIRouter(
    prefix="/services",
    tags=["Services"],
)


@router.get(
    "",
    response_model=list[ServiceResponse],
)
def list_services(
    db: DBSession,
    current_user: User = Depends(get_current_user),
    category_id: UUID | None = Query(default=None),
) -> list[ServiceResponse]:
    service = ServiceService(db)

    services = service.list_services(
        active_only=True,
        category_id=category_id,
    )

    return [
        ServiceResponse.model_validate(item)
        for item in services
    ]


@router.get(
    "/{service_id}",
    response_model=ServiceResponse,
)
def get_service(
    service_id: UUID,
    db: DBSession,
    current_user: User = Depends(get_current_user),
) -> ServiceResponse:
    service = ServiceService(db)

    item = service.get_service(
        service_id=service_id,
    )

    return ServiceResponse.model_validate(item)


@router.post(
    "",
    response_model=ServiceResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_service(
    data: ServiceCreateRequest,
    db: DBSession,
    current_user: Annotated[
        User,
        Depends(require_admin),
    ],
) -> ServiceResponse:
    service = ServiceService(db)

    try:
        item = service.create_service(
            category_id=data.category_id,
            name=data.name,
            slug=data.slug,
            description=data.description,
        )

        db.commit()
        db.refresh(item)

    except Exception:
        db.rollback()
        raise

    return ServiceResponse.model_validate(item)


@router.patch(
    "/{service_id}",
    response_model=ServiceResponse,
)
def update_service(
    service_id: UUID,
    data: ServiceUpdateRequest,
    db: DBSession,
    current_user: Annotated[
        User,
        Depends(require_admin),
    ],
) -> ServiceResponse:
    service = ServiceService(db)

    try:
        item = service.update_service(
            service_id=service_id,
            category_id=data.category_id,
            name=data.name,
            slug=data.slug,
            description=data.description,
        )

        db.commit()
        db.refresh(item)

    except Exception:
        db.rollback()
        raise

    return ServiceResponse.model_validate(item)


@router.post(
    "/{service_id}/activate",
    response_model=ServiceResponse,
)
def activate_service(
    service_id: UUID,
    db: DBSession,
    current_user: Annotated[
        User,
        Depends(require_admin),
    ],
) -> ServiceResponse:
    service = ServiceService(db)

    try:
        item = service.activate_service(
            service_id=service_id,
        )

        db.commit()
        db.refresh(item)

    except Exception:
        db.rollback()
        raise

    return ServiceResponse.model_validate(item)


@router.post(
    "/{service_id}/deactivate",
    response_model=ServiceResponse,
)
def deactivate_service(
    service_id: UUID,
    db: DBSession,
    current_user: Annotated[
        User,
        Depends(require_admin),
    ],
) -> ServiceResponse:
    service = ServiceService(db)

    try:
        item = service.deactivate_service(
            service_id=service_id,
        )

        db.commit()
        db.refresh(item)

    except Exception:
        db.rollback()
        raise

    return ServiceResponse.model_validate(item)


# ------------------------------------------------------------------
# Service requirements
# ------------------------------------------------------------------


@router.get(
    "/{service_id}/requirements",
    response_model=list[ServiceRequirementResponse],
)
def list_service_requirements(
    service_id: UUID,
    db: DBSession,
    current_user: User = Depends(get_current_user),
) -> list[ServiceRequirementResponse]:
    service = ServiceRequirementService(db)

    requirements = service.list_requirements(
        service_id=service_id,
        active_only=True,
    )

    return [
        ServiceRequirementResponse.model_validate(requirement)
        for requirement in requirements
    ]


@router.post(
    "/{service_id}/requirements",
    response_model=ServiceRequirementResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_service_requirement(
    service_id: UUID,
    data: ServiceRequirementCreateRequest,
    db: DBSession,
    current_user: Annotated[
        User,
        Depends(require_admin),
    ],
) -> ServiceRequirementResponse:
    service = ServiceRequirementService(db)

    try:
        requirement = service.create_requirement(
            service_id=service_id,
            key=data.key,
            label=data.label,
            description=data.description,
            requirement_type=data.requirement_type,
            is_required=data.is_required,
            sort_order=data.sort_order,
        )

        db.commit()
        db.refresh(requirement)

    except Exception:
        db.rollback()
        raise

    return ServiceRequirementResponse.model_validate(requirement)


@router.patch(
    "/{service_id}/requirements/{requirement_id}",
    response_model=ServiceRequirementResponse,
)
def update_service_requirement(
    service_id: UUID,
    requirement_id: UUID,
    data: ServiceRequirementUpdateRequest,
    db: DBSession,
    current_user: Annotated[
        User,
        Depends(require_admin),
    ],
) -> ServiceRequirementResponse:
    service = ServiceRequirementService(db)

    try:
        requirement = service.update_requirement(
            service_id=service_id,
            requirement_id=requirement_id,
            key=data.key,
            label=data.label,
            description=data.description,
            requirement_type=data.requirement_type,
            is_required=data.is_required,
            sort_order=data.sort_order,
        )

        db.commit()
        db.refresh(requirement)

    except Exception:
        db.rollback()
        raise

    return ServiceRequirementResponse.model_validate(requirement)


@router.post(
    "/{service_id}/requirements/{requirement_id}/activate",
    response_model=ServiceRequirementResponse,
)
def activate_service_requirement(
    service_id: UUID,
    requirement_id: UUID,
    db: DBSession,
    current_user: Annotated[
        User,
        Depends(require_admin),
    ],
) -> ServiceRequirementResponse:
    service = ServiceRequirementService(db)

    try:
        requirement = service.activate_requirement(
            service_id=service_id,
            requirement_id=requirement_id,
        )

        db.commit()
        db.refresh(requirement)

    except Exception:
        db.rollback()
        raise

    return ServiceRequirementResponse.model_validate(requirement)


@router.post(
    "/{service_id}/requirements/{requirement_id}/deactivate",
    response_model=ServiceRequirementResponse,
)
def deactivate_service_requirement(
    service_id: UUID,
    requirement_id: UUID,
    db: DBSession,
    current_user: Annotated[
        User,
        Depends(require_admin),
    ],
) -> ServiceRequirementResponse:
    service = ServiceRequirementService(db)

    try:
        requirement = service.deactivate_requirement(
            service_id=service_id,
            requirement_id=requirement_id,
        )

        db.commit()
        db.refresh(requirement)

    except Exception:
        db.rollback()
        raise

    return ServiceRequirementResponse.model_validate(requirement)
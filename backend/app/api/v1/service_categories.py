from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.dependencies.authorization import get_current_user, require_admin
from app.dependencies.core import DBSession
from app.models.user import User
from app.schemas.service_category import (
    ServiceCategoryCreateRequest,
    ServiceCategoryResponse,
    ServiceCategoryUpdateRequest,
)
from app.services.service_category_service import ServiceCategoryService


router = APIRouter(
    prefix="/service-categories",
    tags=["Service Categories"],
)


@router.get(
    "",
    response_model=list[ServiceCategoryResponse],
)
def list_service_categories(
    db: DBSession,
    current_user: User = Depends(get_current_user),
) -> list[ServiceCategoryResponse]:
    service = ServiceCategoryService(db)

    categories = service.list_categories(
        active_only=True,
    )

    return [
        ServiceCategoryResponse.model_validate(category)
        for category in categories
    ]


@router.get(
    "/{category_id}",
    response_model=ServiceCategoryResponse,
)
def get_service_category(
    category_id: UUID,
    db: DBSession,
    current_user: User = Depends(get_current_user),
) -> ServiceCategoryResponse:
    service = ServiceCategoryService(db)

    category = service.get_category(
        category_id=category_id,
    )

    return ServiceCategoryResponse.model_validate(category)


@router.post(
    "",
    response_model=ServiceCategoryResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_service_category(
    data: ServiceCategoryCreateRequest,
    db: DBSession,
    current_user: Annotated[
        User,
        Depends(require_admin),
    ],
) -> ServiceCategoryResponse:
    service = ServiceCategoryService(db)

    try:
        category = service.create_category(
            name=data.name,
            slug=data.slug,
            description=data.description,
        )

        db.commit()
        db.refresh(category)

    except Exception:
        db.rollback()
        raise

    return ServiceCategoryResponse.model_validate(category)


@router.patch(
    "/{category_id}",
    response_model=ServiceCategoryResponse,
)
def update_service_category(
    category_id: UUID,
    data: ServiceCategoryUpdateRequest,
    db: DBSession,
    current_user: Annotated[
        User,
        Depends(require_admin),
    ],
) -> ServiceCategoryResponse:
    service = ServiceCategoryService(db)

    try:
        category = service.update_category(
            category_id=category_id,
            name=data.name,
            slug=data.slug,
            description=data.description,
        )

        db.commit()
        db.refresh(category)

    except Exception:
        db.rollback()
        raise

    return ServiceCategoryResponse.model_validate(category)


@router.post(
    "/{category_id}/activate",
    response_model=ServiceCategoryResponse,
)
def activate_service_category(
    category_id: UUID,
    db: DBSession,
    current_user: Annotated[
        User,
        Depends(require_admin),
    ],
) -> ServiceCategoryResponse:
    service = ServiceCategoryService(db)

    try:
        category = service.activate_category(
            category_id=category_id,
        )

        db.commit()
        db.refresh(category)

    except Exception:
        db.rollback()
        raise

    return ServiceCategoryResponse.model_validate(category)


@router.post(
    "/{category_id}/deactivate",
    response_model=ServiceCategoryResponse,
)
def deactivate_service_category(
    category_id: UUID,
    db: DBSession,
    current_user: Annotated[
        User,
        Depends(require_admin),
    ],
) -> ServiceCategoryResponse:
    service = ServiceCategoryService(db)

    try:
        category = service.deactivate_category(
            category_id=category_id,
        )

        db.commit()
        db.refresh(category)

    except Exception:
        db.rollback()
        raise

    return ServiceCategoryResponse.model_validate(category)
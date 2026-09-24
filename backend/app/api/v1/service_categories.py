from fastapi import APIRouter

from app.dependencies.core import DBSession
from app.repositories.service_category_repository import (
    ServiceCategoryRepository,
)
from app.schemas.service_category import (
    ServiceCategoryResponse,
    ServiceCategorRequest
)
from app.models.service_category import ServiceCategory

router = APIRouter(
    prefix="/service-categories",
    tags=["service-categories"],
)


@router.get(
    "",
    response_model=list[ServiceCategoryResponse],
)
def list_service_categories(
    db: DBSession,
) -> list[ServiceCategoryResponse]:
    repository = ServiceCategoryRepository(db)

    return repository.list_active()

@router.post(
    "/create",
    response_model=ServiceCategoryResponse,
)
def create_service_categories(
    db: DBSession,
    request: ServiceCategorRequest,
) -> ServiceCategoryResponse:

    service_category = ServiceCategory(
        name=request.name,
        slug=request.slug,
        description=request.description,
    )

    repository = ServiceCategoryRepository(db)
    new_service_category = repository.create(service_category)

    return new_service_category
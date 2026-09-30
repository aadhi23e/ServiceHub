from uuid import uuid4

import pytest

from app.core.exceptions import ResourceConflictError
from app.core.exceptions import ResourceNotFoundError
from app.services.service_category_service import ServiceCategoryService


def test_get_category_raises_when_missing(db):
    service = ServiceCategoryService(db)

    with pytest.raises(ResourceNotFoundError):
        service.get_category(
            category_id=uuid4(),
        )


def test_create_category_normalizes_slug(db):
    service = ServiceCategoryService(db)

    category = service.create_category(
        name="Home Maintenance",
        slug=" Home-Maintenance ",
        description="Home maintenance services",
    )

    assert category.slug == "home-maintenance"
    assert category.name == "Home Maintenance"


def test_duplicate_category_slug_is_rejected(db):
    service = ServiceCategoryService(db)

    service.create_category(
        name="Home Maintenance",
        slug="home-maintenance",
        description=None,
    )

    with pytest.raises(ResourceConflictError):
        service.create_category(
            name="Another Category",
            slug="home-maintenance",
            description=None,
        )
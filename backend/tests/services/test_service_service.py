from uuid import uuid4

import pytest

from app.core.exceptions import ResourceConflictError
from app.core.exceptions import ResourceNotFoundError
from app.services.service_service import ServiceService
from app.services.service_category_service import ServiceCategoryService


def test_create_service_requires_existing_category(db):
    service = ServiceService(db)

    with pytest.raises(ResourceNotFoundError):
        service.create_service(
            category_id=uuid4(),
            name="AC Repair",
            slug="ac-repair",
            description=None,
        )


def test_create_service(db):
    category_service = ServiceCategoryService(db)

    category = category_service.create_category(
        name="Home Maintenance",
        slug="home-maintenance",
        description=None,
    )

    service = ServiceService(db)

    item = service.create_service(
        category_id=category.id,
        name="AC Repair",
        slug="ac-repair",
        description="Air conditioner repair",
    )

    assert item.category_id == category.id
    assert item.slug == "ac-repair"


def test_service_cannot_be_created_under_inactive_category(db):
    category_service = ServiceCategoryService(db)

    category = category_service.create_category(
        name="Home Maintenance",
        slug="home-maintenance",
        description=None,
    )

    category_service.deactivate_category(
        category_id=category.id,
    )

    service = ServiceService(db)

    with pytest.raises(ResourceConflictError):
        service.create_service(
            category_id=category.id,
            name="AC Repair",
            slug="ac-repair",
            description=None,
        )
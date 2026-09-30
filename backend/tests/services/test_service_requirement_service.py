import pytest

from app.enums.servicehub import ServiceRequirementType
from app.core.exceptions import ResourceConflictError
from app.services.service_category_service import ServiceCategoryService
from app.services.service_service import ServiceService
from app.services.service_requirement_service import (
    ServiceRequirementService,
)


def create_service(db):
    category_service = ServiceCategoryService(db)

    category = category_service.create_category(
        name="Home Maintenance",
        slug="home-maintenance",
        description=None,
    )

    service_service = ServiceService(db)

    return service_service.create_service(
        category_id=category.id,
        name="AC Repair",
        slug="ac-repair",
        description=None,
    )


def test_create_requirement(db):
    service = create_service(db)

    requirement_service = ServiceRequirementService(db)

    requirement = requirement_service.create_requirement(
        service_id=service.id,
        key="problem",
        label="What is the problem?",
        description=None,
        requirement_type=ServiceRequirementType.TEXT,
        is_required=True,
        sort_order=0,
    )

    assert requirement.service_id == service.id
    assert requirement.key == "problem"
    assert requirement.is_required is True


def test_duplicate_requirement_key_is_rejected(db):
    service = create_service(db)

    requirement_service = ServiceRequirementService(db)

    requirement_service.create_requirement(
        service_id=service.id,
        key="problem",
        label="Problem",
        description=None,
        requirement_type=ServiceRequirementType.TEXT,
        is_required=True,
        sort_order=0,
    )

    with pytest.raises(ResourceConflictError):
        requirement_service.create_requirement(
            service_id=service.id,
            key="problem",
            label="Another Problem",
            description=None,
            requirement_type=ServiceRequirementType.TEXT,
            is_required=False,
            sort_order=1,
        )
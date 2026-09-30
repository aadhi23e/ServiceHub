from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.enums.service import ServiceMode, ServiceStatus


class ServiceRequirementResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    description: str | None
    requirement_type: str
    is_required: bool
    display_order: int
    options: dict | None


class ServiceCreateRequest(BaseModel):
    category_id: UUID

    name: str = Field(
        min_length=1,
        max_length=150,
    )

    description: str | None = None

    price: Decimal = Field(
        ge=0,
        max_digits=12,
        decimal_places=2,
    )

    currency: str = Field(
        default="INR",
        min_length=3,
        max_length=3,
    )

    duration_minutes: int = Field(
        gt=0,
        le=1440,
    )

    buffer_minutes: int = Field(
        default=0,
        ge=0,
        le=1440,
    )

    service_modes: list[ServiceMode] = Field(
        min_length=1,
    )


class ServiceUpdateRequest(BaseModel):
    category_id: UUID | None = None

    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=150,
    )

    description: str | None = None

    price: Decimal | None = Field(
        default=None,
        ge=0,
        max_digits=12,
        decimal_places=2,
    )

    currency: str | None = Field(
        default=None,
        min_length=3,
        max_length=3,
    )

    duration_minutes: int | None = Field(
        default=None,
        gt=0,
        le=1440,
    )

    buffer_minutes: int | None = Field(
        default=None,
        ge=0,
        le=1440,
    )

    service_modes: list[ServiceMode] | None = Field(
        default=None,
        min_length=1,
    )


class ServiceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    category_id: UUID

    name: str
    description: str | None

    price: Decimal
    currency: str

    duration_minutes: int
    buffer_minutes: int

    status: ServiceStatus
    service_modes: list[ServiceMode]

    created_at: object
    updated_at: object


class ServiceListResponse(BaseModel):
    items: list[ServiceResponse]
    page: int
    page_size: int
    total: int
    total_pages: int
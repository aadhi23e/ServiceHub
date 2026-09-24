from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class ServiceCreateRequest(BaseModel):
    category_id: int = Field(gt=0)

    name: str = Field(
        min_length=1,
        max_length=200,
    )

    description: str | None = Field(
        default=None,
        max_length=5000,
    )

    duration_minutes: int = Field(
        gt=0,
        le=1440,
    )

    price: Decimal = Field(
        ge=0,
        max_digits=10,
        decimal_places=2,
    )


class ServiceUpdateRequest(BaseModel):
    category_id: int | None = Field(
        default=None,
        gt=0,
    )

    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=200,
    )

    description: str | None = Field(
        default=None,
        max_length=5000,
    )

    duration_minutes: int | None = Field(
        default=None,
        gt=0,
        le=1440,
    )

    price: Decimal | None = Field(
        default=None,
        ge=0,
        max_digits=10,
        decimal_places=2,
    )


class ServiceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    provider_id: int
    category_id: int
    name: str
    description: str | None
    duration_minutes: int
    price: Decimal
    is_active: bool
    created_at: datetime
    updated_at: datetime


class ServiceListResponse(BaseModel):
    items: list[ServiceResponse]
    total: int
    offset: int
    limit: int

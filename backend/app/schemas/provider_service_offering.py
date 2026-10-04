from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ProviderServiceOfferingCreateRequest(BaseModel):
    service_id: UUID

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

    service_modes: list[str] = Field(
        min_length=1,
    )

    @field_validator("currency")
    @classmethod
    def validate_currency(cls, value: str) -> str:
        return value.upper().strip()

    @field_validator("service_modes")
    @classmethod
    def validate_service_modes(
        cls,
        value: list[str],
    ) -> list[str]:
        modes = [mode.strip().upper() for mode in value]

        if not modes:
            raise ValueError("At least one service mode is required.")

        if any(not mode for mode in modes):
            raise ValueError("Service modes cannot be empty.")

        if len(modes) != len(set(modes)):
            raise ValueError("Service modes must be unique.")

        return modes


class ProviderServiceOfferingUpdateRequest(BaseModel):
    service_id: UUID | None = None

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

    service_modes: list[str] | None = Field(
        default=None,
        min_length=1,
    )

    @field_validator("currency")
    @classmethod
    def validate_currency(cls, value: str | None) -> str | None:
        if value is None:
            return None

        return value.upper().strip()

    @field_validator("service_modes")
    @classmethod
    def validate_service_modes(
        cls,
        value: list[str] | None,
    ) -> list[str] | None:
        if value is None:
            return None

        modes = [mode.strip().upper() for mode in value]

        if not modes:
            raise ValueError("At least one service mode is required.")

        if any(not mode for mode in modes):
            raise ValueError("Service modes cannot be empty.")

        if len(modes) != len(set(modes)):
            raise ValueError("Service modes must be unique.")

        return modes


class ProviderServiceOfferingServiceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    slug: str
    category_id: UUID


class ProviderServiceOfferingResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    service_id: UUID

    service: ProviderServiceOfferingServiceResponse

    price: Decimal
    currency: str
    duration_minutes: int
    buffer_minutes: int
    service_modes: list[str]

    is_active: bool

    created_at: datetime
    updated_at: datetime


class ProviderServiceOfferingListResponse(BaseModel):
    items: list[ProviderServiceOfferingResponse]

    page: int
    page_size: int
    total: int
    total_pages: int
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ProviderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    business_name: str
    description: str | None
    phone: str | None
    address: str | None
    city: str | None
    status: str
    timezone: str
    created_at: datetime
    updated_at: datetime


class ProviderUpdateRequest(BaseModel):
    business_name: str | None = Field(
        default=None,
        min_length=1,
        max_length=200,
    )

    description: str | None = Field(
        default=None,
        max_length=5000,
    )

    phone: str | None = Field(
        default=None,
        max_length=30,
    )

    address: str | None = Field(
        default=None,
        max_length=500,
    )

    city: str | None = Field(
        default=None,
        max_length=100,
    )

    timezone: str | None = Field(
        default=None,
        max_length=100,
    )
# backend/app/schemas/address.py

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class AddressCreateRequest(BaseModel):
    """
    Data required to create a physical address for the authenticated user.
    """

    address_line_1: str = Field(min_length=1, max_length=255)
    address_line_2: str | None = Field(default=None, max_length=255)
    landmark: str | None = Field(default=None, max_length=255)
    city: str = Field(min_length=1, max_length=100)
    state: str = Field(min_length=1, max_length=100)
    postal_code: str = Field(min_length=3, max_length=20)
    country_code: str = Field(default="IN", min_length=2, max_length=2)
    latitude: float | None = Field(default=None, ge=-90, le=90)
    longitude: float | None = Field(default=None, ge=-180, le=180)

    label: str | None = Field(default=None, max_length=50)
    is_default: bool = False


class AddressUpdateRequest(BaseModel):
    """
    Fields that can be changed on a user's saved address.
    """

    address_line_1: str | None = Field(default=None, min_length=1, max_length=255)
    address_line_2: str | None = Field(default=None, max_length=255)
    landmark: str | None = Field(default=None, max_length=255)
    city: str | None = Field(default=None, min_length=1, max_length=100)
    state: str | None = Field(default=None, min_length=1, max_length=100)
    postal_code: str | None = Field(default=None, min_length=3, max_length=20)
    country_code: str | None = Field(default=None, min_length=2, max_length=2)
    latitude: float | None = Field(default=None, ge=-90, le=90)
    longitude: float | None = Field(default=None, ge=-180, le=180)
    label: str | None = Field(default=None, max_length=50)


class AddressResponse(BaseModel):
    """
    Address returned to the authenticated owner.
    """

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    address_line_1: str
    address_line_2: str | None
    landmark: str | None
    city: str
    state: str
    postal_code: str
    country_code: str
    latitude: float | None
    longitude: float | None
    label: str | None
    is_default: bool
    created_at: datetime
    updated_at: datetime
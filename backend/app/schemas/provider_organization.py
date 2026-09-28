from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.enums.provider import ProviderStatus


class ProviderOrganizationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    legal_name: str | None
    description: str | None
    status: ProviderStatus
    created_by: UUID
    created_at: datetime
    updated_at: datetime

class ProviderOrganizationUpdateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=150,
    )

    legal_name: str | None = Field(
        default=None,
        max_length=200,
    )

    description: str | None = Field(
        default=None,
        max_length=2000,
    )

class ProviderOrganizationListItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    status: ProviderStatus

class ProviderOrganizationListResponse(BaseModel):
    items: list[ProviderOrganizationListItem]
    total: int

class ProviderOrganizationSummaryResponse(BaseModel):
    id: UUID
    name: str
    status: ProviderStatus

    member_count: int
    location_count: int
    service_count: int
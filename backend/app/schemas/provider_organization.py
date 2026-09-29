from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.enums.provider import ProviderStatus


# Return public organization information.
class ProviderOrganizationPublicResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    description: str | None


# Return a paginated list of public organizations.
class ProviderOrganizationPublicListResponse(BaseModel):
    items: list[ProviderOrganizationPublicResponse]
    page: int
    page_size: int
    total: int
    total_pages: int


# Return the authenticated provider's organization.
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


# Update organization information.
class ProviderOrganizationUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=255,
    )
    legal_name: str | None = Field(
        default=None,
        max_length=255,
    )
    description: str | None = Field(
        default=None,
        max_length=2000,
    )


# Return an organization to an administrator.
class ProviderOrganizationAdminResponse(
    ProviderOrganizationResponse,
):
    pass


# Return an organization in an admin list.
class ProviderOrganizationAdminListItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    legal_name: str | None
    status: ProviderStatus
    created_by: UUID
    created_at: datetime


# Return a paginated admin organization list.
class ProviderOrganizationAdminListResponse(BaseModel):
    items: list[ProviderOrganizationAdminListItem]
    page: int
    page_size: int
    total: int
    total_pages: int


# Return administrative organization statistics.
class ProviderOrganizationAdminSummary(BaseModel):
    id: UUID
    name: str
    status: ProviderStatus
    member_count: int

# Create a provider organization for the authenticated customer.
class ProviderOrganizationCreate(BaseModel):
    organization_name: str = Field(
        min_length=2,
        max_length=255,
    )
    legal_name: str | None = Field(
        default=None,
        max_length=255,
    )
    display_name: str = Field(
        min_length=2,
        max_length=255,
    )
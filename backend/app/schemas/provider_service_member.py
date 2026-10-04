from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr


class ProviderServiceMemberCreateRequest(BaseModel):
    provider_membership_id: UUID


class ProviderServiceMemberResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    provider_service_offering_id: UUID
    provider_membership_id: UUID
    user_id: UUID
    first_name: str
    last_name: str
    email: EmailStr
    is_active: bool
    created_at: datetime
    updated_at: datetime


class ProviderServiceMemberListResponse(BaseModel):
    items: list[ProviderServiceMemberResponse]
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.enums.servicehub import VerificationStatus


class ProviderVerificationRejectRequest(BaseModel):
    reason: str = Field(
        min_length=5,
        max_length=2000,
    )


class ProviderVerificationResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: UUID
    organization_id: UUID
    reviewed_by: UUID | None
    status: VerificationStatus
    document_reference: str | None
    notes: str | None
    rejection_reason: str | None
    reviewed_at: datetime | None
    expires_at: datetime | None
    created_at: datetime
    updated_at: datetime

class ProviderVerificationListResponse(BaseModel):
    items: list[ProviderVerificationResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
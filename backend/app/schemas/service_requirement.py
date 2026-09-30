from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.enums.servicehub import ServiceRequirementType


class ServiceRequirementCreateRequest(BaseModel):
    key: str = Field(min_length=1, max_length=100)
    label: str = Field(min_length=1, max_length=150)
    description: str | None = None
    requirement_type: ServiceRequirementType
    is_required: bool = False
    sort_order: int = Field(default=0, ge=0)


class ServiceRequirementUpdateRequest(BaseModel):
    key: str | None = Field(default=None, min_length=1, max_length=100)
    label: str | None = Field(default=None, min_length=1, max_length=150)
    description: str | None = None
    requirement_type: ServiceRequirementType | None = None
    is_required: bool | None = None
    sort_order: int | None = Field(default=None, ge=0)


class ServiceRequirementResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    service_id: UUID
    key: str
    label: str
    description: str | None
    requirement_type: ServiceRequirementType
    is_required: bool
    sort_order: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
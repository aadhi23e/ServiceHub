from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ServiceCreateRequest(BaseModel):
    category_id: UUID

    name: str = Field(
        min_length=1,
        max_length=150,
    )

    slug: str = Field(
        min_length=1,
        max_length=150,
    )

    description: str | None = None


class ServiceUpdateRequest(BaseModel):
    category_id: UUID | None = None

    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=150,
    )

    slug: str | None = Field(
        default=None,
        min_length=1,
        max_length=150,
    )

    description: str | None = None


class ServiceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    category_id: UUID

    name: str
    slug: str
    description: str | None

    is_active: bool

    created_at: object
    updated_at: object


class ServiceListResponse(BaseModel):
    items: list[ServiceResponse]
    page: int
    page_size: int
    total: int
    total_pages: int
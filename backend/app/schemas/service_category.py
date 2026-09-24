from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ServiceCategoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    slug: str
    description: str | None
    is_active: bool
    created_at: datetime
    updated_at: datetime

class ServiceCategorRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    slug: str
    description: str | None

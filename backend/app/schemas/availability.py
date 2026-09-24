from datetime import time

from pydantic import BaseModel, ConfigDict, Field, model_validator


class AvailabilityCreateRequest(BaseModel):
    day_of_week: int = Field(
        ge=0,
        le=6,
    )

    start_time: time
    end_time: time

    is_active: bool = True

    @model_validator(mode="after")
    def validate_time_range(self):
        if self.start_time >= self.end_time:
            raise ValueError(
                "start_time must be earlier than end_time."
            )

        return self


class AvailabilityUpdateRequest(BaseModel):
    day_of_week: int | None = Field(
        default=None,
        ge=0,
        le=6,
    )

    start_time: time | None = None
    end_time: time | None = None
    is_active: bool | None = None


class AvailabilityResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    provider_id: int
    day_of_week: int
    start_time: time
    end_time: time
    is_active: bool
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.enums.booking import BookingStatus


class BookingCreateRequest(BaseModel):
    provider_id: int = Field(gt=0)
    service_id: int = Field(gt=0)

    start_at: datetime
    end_at: datetime

    customer_notes: str | None = Field(
        default=None,
        max_length=5000,
    )

    @field_validator("start_at", "end_at")
    @classmethod
    def validate_timezone(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("Datetime must include timezone information.")
        return value

    @field_validator("end_at")
    @classmethod
    def validate_time_range(
        cls,
        end_at: datetime,
        info,
    ) -> datetime:
        start_at = info.data.get("start_at")

        if start_at is not None and end_at <= start_at:
            raise ValueError("end_at must be later than start_at.")

        return end_at


class BookingResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int

    customer_id: int
    provider_id: int
    service_id: int

    start_at: datetime
    end_at: datetime

    status: BookingStatus

    customer_notes: str | None
    provider_notes: str | None

    created_at: datetime
    updated_at: datetime

    cancelled_at: datetime | None
    completed_at: datetime | None

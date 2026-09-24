from datetime import time

from sqlalchemy.orm import Session

from app.core.exceptions import (
    ConflictError,
    ResourceNotFoundError,
)
from app.models.availability import Availability
from app.models.provider import ProviderProfile
from app.repositories.availability_repository import (
    AvailabilityRepository,
)
from app.schemas.availability import (
    AvailabilityCreateRequest,
    AvailabilityUpdateRequest,
)


class AvailabilityService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.repository = AvailabilityRepository(db)

    def list(
        self,
        provider: ProviderProfile,
    ) -> list[Availability]:
        return self.repository.list_by_provider(provider.id)

    def _check_overlap(
        self,
        provider_id: int,
        day_of_week: int,
        start_time: time,
        end_time: time,
        *,
        exclude_id: int | None = None,
    ) -> None:
        existing = self.repository.list_by_day(
            provider_id,
            day_of_week,
        )

        for item in existing:
            if exclude_id is not None and item.id == exclude_id:
                continue

            overlaps = start_time < item.end_time and end_time > item.start_time

            if overlaps:
                raise ConflictError(
                    message=(
                        "The availability period overlaps "
                        "with an existing availability period."
                    ),
                    code="AVAILABILITY_OVERLAP",
                )

    def create(
        self,
        provider: ProviderProfile,
        request: AvailabilityCreateRequest,
    ) -> Availability:
        self._check_overlap(
            provider.id,
            request.day_of_week,
            request.start_time,
            request.end_time,
        )

        availability = Availability(
            provider_id=provider.id,
            day_of_week=request.day_of_week,
            start_time=request.start_time,
            end_time=request.end_time,
            is_active=request.is_active,
        )

        self.repository.create(availability)

        self.db.commit()
        self.db.refresh(availability)

        return availability

    def update(
        self,
        provider: ProviderProfile,
        availability_id: int,
        request: AvailabilityUpdateRequest,
    ) -> Availability:
        availability = self.repository.get_by_id_for_provider(
            availability_id,
            provider.id,
        )

        if availability is None:
            raise ResourceNotFoundError(
                message="Availability not found.",
                code="AVAILABILITY_NOT_FOUND",
            )

        day_of_week = (
            request.day_of_week
            if request.day_of_week is not None
            else availability.day_of_week
        )

        start_time = (
            request.start_time
            if request.start_time is not None
            else availability.start_time
        )

        end_time = (
            request.end_time if request.end_time is not None else availability.end_time
        )

        if start_time >= end_time:
            raise ConflictError(
                message="start_time must be earlier than end_time.",
                code="INVALID_AVAILABILITY_RANGE",
            )

        if (
            day_of_week != availability.day_of_week
            or start_time != availability.start_time
            or end_time != availability.end_time
        ):
            self._check_overlap(
                provider.id,
                day_of_week,
                start_time,
                end_time,
                exclude_id=availability.id,
            )

        updated = self.repository.update(
            availability,
            day_of_week=request.day_of_week,
            start_time=request.start_time,
            end_time=request.end_time,
            is_active=request.is_active,
        )

        self.db.commit()
        self.db.refresh(updated)

        return updated

    def set_active(
        self,
        provider: ProviderProfile,
        availability_id: int,
        is_active: bool,
    ) -> Availability:
        availability = self.repository.get_by_id_for_provider(
            availability_id,
            provider.id,
        )

        if availability is None:
            raise ResourceNotFoundError(
                message="Availability not found.",
                code="AVAILABILITY_NOT_FOUND",
            )

        if is_active:
            self._check_overlap(
                provider.id,
                availability.day_of_week,
                availability.start_time,
                availability.end_time,
                exclude_id=availability.id,
            )

        self.repository.update(
            availability,
            is_active=is_active,
        )

        self.db.commit()
        self.db.refresh(availability)

        return availability

    def delete(
        self,
        provider: ProviderProfile,
        availability_id: int,
    ) -> None:
        availability = self.repository.get_by_id_for_provider(
            availability_id,
            provider.id,
        )

        if availability is None:
            raise ResourceNotFoundError(
                message="Availability not found.",
                code="AVAILABILITY_NOT_FOUND",
            )

        self.repository.delete(availability)

        self.db.commit()

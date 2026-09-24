from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.availability import Availability


class AvailabilityRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id_for_provider(
        self,
        availability_id: int,
        provider_id: int,
    ) -> Availability | None:
        statement = select(Availability).where(
            Availability.id == availability_id,
            Availability.provider_id == provider_id,
        )

        return self.db.scalar(statement)

    def list_by_provider(
        self,
        provider_id: int,
    ) -> list[Availability]:
        statement = (
            select(Availability)
            .where(
                Availability.provider_id == provider_id,
            )
            .order_by(
                Availability.day_of_week,
                Availability.start_time,
            )
        )

        return list(self.db.scalars(statement).all())

    def list_by_day(
        self,
        provider_id: int,
        day_of_week: int,
    ) -> list[Availability]:
        statement = select(Availability).where(
            Availability.provider_id == provider_id,
            Availability.day_of_week == day_of_week,
            Availability.is_active.is_(True),
        )

        return list(self.db.scalars(statement).all())

    def create(
        self,
        availability: Availability,
    ) -> Availability:
        self.db.add(availability)
        self.db.flush()

        return availability

    def update(
        self,
        availability: Availability,
        *,
        day_of_week: int | None = None,
        start_time=None,
        end_time=None,
        is_active: bool | None = None,
    ) -> Availability:
        if day_of_week is not None:
            availability.day_of_week = day_of_week

        if start_time is not None:
            availability.start_time = start_time

        if end_time is not None:
            availability.end_time = end_time

        if is_active is not None:
            availability.is_active = is_active

        self.db.flush()

        return availability

    def delete(
        self,
        availability: Availability,
    ) -> None:
        self.db.delete(availability)
        self.db.flush()
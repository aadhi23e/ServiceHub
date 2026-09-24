from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.enums.booking import BookingStatus
from app.models.booking import Booking
from app.models.provider import ProviderProfile
from app.models.service import Service


class BookingRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, booking_id: int) -> Booking | None:
        statement = (
            select(Booking)
            .options(
                joinedload(Booking.customer),
                joinedload(Booking.provider),
                joinedload(Booking.service),
            )
            .where(Booking.id == booking_id)
        )

        return self.db.scalar(statement)

    def get_provider_profile_by_user_id(
        self,
        user_id: int,
    ) -> ProviderProfile | None:
        statement = select(ProviderProfile).where(ProviderProfile.user_id == user_id)

        return self.db.scalar(statement)

    def get_service(
        self,
        *,
        provider_id: int,
        service_id: int,
    ) -> Service | None:
        statement = select(Service).where(
            Service.provider_id == provider_id,
            Service.id == service_id,
        )

        return self.db.scalar(statement)

    def create(self, booking: Booking) -> Booking:
        self.db.add(booking)
        self.db.flush()

        return booking

    def list_customer_bookings(
        self,
        *,
        customer_id: int,
    ) -> list[Booking]:
        statement = (
            select(Booking)
            .options(
                joinedload(Booking.customer),
                joinedload(Booking.provider),
                joinedload(Booking.service),
            )
            .where(Booking.customer_id == customer_id)
            .order_by(Booking.created_at.desc())
        )

        return list(self.db.scalars(statement).unique().all())

    def list_provider_bookings(
        self,
        *,
        provider_id: int,
    ) -> list[Booking]:
        statement = (
            select(Booking)
            .options(
                joinedload(Booking.customer),
                joinedload(Booking.provider),
                joinedload(Booking.service),
            )
            .where(Booking.provider_id == provider_id)
            .order_by(Booking.start_at.asc())
        )

        return list(self.db.scalars(statement).unique().all())

    def list_all_bookings(self) -> list[Booking]:
        statement = (
            select(Booking)
            .options(
                joinedload(Booking.customer),
                joinedload(Booking.provider),
                joinedload(Booking.service),
            )
            .order_by(Booking.created_at.desc())
        )

        return list(self.db.scalars(statement).unique().all())

    def update_status(
        self,
        booking: Booking,
        *,
        status: BookingStatus,
    ) -> Booking:
        booking.status = status.value
        self.db.flush()

        return booking

    def mark_cancelled(
        self,
        booking: Booking,
    ) -> Booking:
        booking.status = BookingStatus.CANCELLED.value
        booking.cancelled_at = datetime.now(tz=booking.start_at.tzinfo)

        self.db.flush()

        return booking

    def mark_completed(
        self,
        booking: Booking,
    ) -> Booking:
        booking.status = BookingStatus.COMPLETED.value
        booking.completed_at = datetime.now(tz=booking.start_at.tzinfo)

        self.db.flush()

        return booking

from datetime import datetime, timezone

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.exceptions import (
    AuthorizationError,
    ConflictError,
    ResourceNotFoundError,
    ValidationError,
)
from app.enums.booking import BookingStatus
from app.enums.user import UserRole
from app.models.booking import Booking
from app.models.user import User
from app.repositories.booking_repository import BookingRepository
from app.schemas.booking import BookingCreateRequest


class BookingService:
    def __init__(self, db: Session) -> None:
        self.repository = BookingRepository(db)
        self.db = db

    def create_booking(
        self,
        *,
        customer: User,
        request: BookingCreateRequest,
    ) -> Booking:
        if request.start_at <= datetime.now(timezone.utc):
            raise ValidationError(
                message="Booking start time must be in the future.",
                code="BOOKING_START_TIME_INVALID",
            )

        requested_service = self.repository.get_service(
            provider_id=request.provider_id,
            service_id=request.service_id,
        )

        if requested_service is None:
            raise ResourceNotFoundError(
                message="The requested service was not found for this provider.",
                code="SERVICE_NOT_FOUND",
            )

        booking = Booking(
            customer_id=customer.id,
            provider_id=request.provider_id,
            service_id=request.service_id,
            start_at=request.start_at,
            end_at=request.end_at,
            status=BookingStatus.PENDING.value,
            customer_notes=request.customer_notes,
        )

        try:
            return self.repository.create(booking)
        except IntegrityError as exc:
            self.db.rollback()

            constraint_name = getattr(
                getattr(exc.orig, "diag", None),
                "constraint_name",
                None,
            )

            if constraint_name == "no_provider_overlapping_bookings":
                raise ConflictError(
                    message="The provider is already booked during this time.",
                    code="BOOKING_TIME_CONFLICT",
                ) from exc

            raise ConflictError(
                message="The booking could not be created because it conflicts with existing data.",
                code="BOOKING_CREATE_CONFLICT",
            ) from exc

    def get_customer_bookings(
        self,
        *,
        customer_id: int,
    ) -> list[Booking]:
        return self.repository.list_customer_bookings(
            customer_id=customer_id,
        )

    def get_provider_bookings(
        self,
        *,
        provider_user_id: int,
    ) -> list[Booking]:
        provider = self.repository.get_provider_profile_by_user_id(provider_user_id)

        if provider is None:
            raise ResourceNotFoundError(
                message="Provider profile not found.",
                code="PROVIDER_PROFILE_NOT_FOUND",
            )

        return self.repository.list_provider_bookings(
            provider_id=provider.id,
        )

    def list_all_bookings(self) -> list[Booking]:
        return self.repository.list_all_bookings()

    def get_booking_for_user(
        self,
        *,
        booking_id: int,
        user: User,
    ) -> Booking:
        booking = self._get_booking(booking_id)

        if user.role == UserRole.ADMIN.value:
            return booking

        if user.role == UserRole.CUSTOMER.value and booking.customer_id == user.id:
            return booking

        if user.role == UserRole.PROVIDER.value:
            provider = self.repository.get_provider_profile_by_user_id(user.id)

            if provider is not None and booking.provider_id == provider.id:
                return booking

        raise AuthorizationError(
            message="You do not have permission to access this booking.",
            code="BOOKING_ACCESS_FORBIDDEN",
        )

    def confirm_booking(
        self,
        *,
        booking_id: int,
        user: User,
    ) -> Booking:
        booking = self._get_booking(booking_id)
        self._require_provider_or_admin(user, booking)

        self._require_status(
            booking,
            allowed={BookingStatus.PENDING},
            action="confirm",
        )

        return self.repository.update_status(
            booking,
            status=BookingStatus.CONFIRMED,
        )

    def reject_booking(
        self,
        *,
        booking_id: int,
        user: User,
    ) -> Booking:
        booking = self._get_booking(booking_id)
        self._require_provider_or_admin(user, booking)

        self._require_status(
            booking,
            allowed={BookingStatus.PENDING},
            action="reject",
        )

        return self.repository.update_status(
            booking,
            status=BookingStatus.REJECTED,
        )

    def start_booking(
        self,
        *,
        booking_id: int,
        user: User,
    ) -> Booking:
        booking = self._get_booking(booking_id)
        self._require_provider_or_admin(user, booking)

        self._require_status(
            booking,
            allowed={BookingStatus.CONFIRMED},
            action="start",
        )

        return self.repository.update_status(
            booking,
            status=BookingStatus.IN_PROGRESS,
        )

    def complete_booking(
        self,
        *,
        booking_id: int,
        user: User,
    ) -> Booking:
        booking = self._get_booking(booking_id)
        self._require_provider_or_admin(user, booking)

        self._require_status(
            booking,
            allowed={BookingStatus.IN_PROGRESS},
            action="complete",
        )

        return self.repository.mark_completed(booking)

    def cancel_booking(
        self,
        *,
        booking_id: int,
        user: User,
    ) -> Booking:
        booking = self._get_booking(booking_id)

        if user.role == UserRole.ADMIN.value:
            pass

        elif user.role == UserRole.CUSTOMER.value:
            if booking.customer_id != user.id:
                raise AuthorizationError(
                    message="You do not have permission to cancel this booking.",
                    code="BOOKING_CANCEL_FORBIDDEN",
                )

        elif user.role == UserRole.PROVIDER.value:
            provider = self.repository.get_provider_profile_by_user_id(user.id)

            if provider is None or booking.provider_id != provider.id:
                raise AuthorizationError(
                    message="You do not have permission to cancel this booking.",
                    code="BOOKING_CANCEL_FORBIDDEN",
                )

        else:
            raise AuthorizationError(
                message="You do not have permission to cancel this booking.",
                code="BOOKING_CANCEL_FORBIDDEN",
            )

        self._require_status(
            booking,
            allowed={
                BookingStatus.PENDING,
                BookingStatus.CONFIRMED,
            },
            action="cancel",
        )

        return self.repository.mark_cancelled(booking)

    def _get_booking(self, booking_id: int) -> Booking:
        booking = self.repository.get_by_id(booking_id)

        if booking is None:
            raise ResourceNotFoundError(
                message="Booking not found.",
                code="BOOKING_NOT_FOUND",
            )

        return booking

    def _require_provider_or_admin(
        self,
        user: User,
        booking: Booking,
    ) -> None:
        if user.role == UserRole.ADMIN.value:
            return

        if user.role != UserRole.PROVIDER.value:
            raise AuthorizationError(
                message="You do not have permission to modify this booking.",
                code="BOOKING_MODIFICATION_FORBIDDEN",
            )

        provider = self.repository.get_provider_profile_by_user_id(user.id)

        if provider is None or booking.provider_id != provider.id:
            raise AuthorizationError(
                message="You do not have permission to modify this booking.",
                code="BOOKING_MODIFICATION_FORBIDDEN",
            )

    def _require_status(
        self,
        booking: Booking,
        *,
        allowed: set[BookingStatus],
        action: str,
    ) -> None:
        current_status = BookingStatus(booking.status)

        if current_status not in allowed:
            allowed_values = ", ".join(status.value for status in allowed)

            raise ConflictError(
                message=(
                    f"Booking cannot be {action}ed while it is "
                    f"{current_status.value}. "
                    f"Allowed states: {allowed_values}."
                ),
                code="INVALID_BOOKING_STATE",
            )

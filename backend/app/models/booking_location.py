from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import DateTime, ForeignKey, Index, Numeric, String, func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.booking import Booking


class BookingLocation(Base):
    __tablename__ = "booking_locations"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    booking_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("bookings.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )

    address_line_1: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    address_line_2: Mapped[str | None] = mapped_column(
        String(255),
    )

    landmark: Mapped[str | None] = mapped_column(
        String(255),
    )

    city: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    state: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    postal_code: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    country_code: Mapped[str] = mapped_column(
        String(2),
        default="IN",
        nullable=False,
    )

    latitude: Mapped[float | None] = mapped_column(
        Numeric(9, 6),
    )

    longitude: Mapped[float | None] = mapped_column(
        Numeric(9, 6),
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    booking: Mapped["Booking"] = relationship(
        back_populates="location",
    )

    __table_args__ = (
        Index(
            "ix_booking_locations_booking_id",
            "booking_id",
        ),
        Index(
            "ix_booking_locations_postal_code",
            "postal_code",
        ),
    )
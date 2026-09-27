from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Index,
    Numeric,
    String,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Enum as SAEnum

from app.enums.servicehub import BookingStatus, ServiceMode
from app.db.base import Base

if TYPE_CHECKING:
    from app.models.booking_assignment import BookingAssignment
    from app.models.booking_location import BookingLocation
    from app.models.booking_status_history import BookingStatusHistory
    from app.models.booking_travel import BookingTravel
    from app.models.dispute import Dispute
    from app.models.invoice import Invoice
    from app.models.payment import Payment
    from app.models.provider_organization import ProviderOrganization
    from app.models.review import Review
    from app.models.service import Service
    from app.models.service_issue import ServiceIssue
    from app.models.user import User


class Booking(Base):
    __tablename__ = "bookings"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    customer_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False,
    )

    organization_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("provider_organizations.id", ondelete="RESTRICT"),
        nullable=False,
    )

    service_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("services.id", ondelete="RESTRICT"),
        nullable=False,
    )

    service_mode: Mapped[ServiceMode] = mapped_column(
        SAEnum(
            ServiceMode,
            name="service_mode",
            native_enum=True,
            create_type=False,
        ),
        nullable=False,
    )

    scheduled_start: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    scheduled_end: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    price: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    currency: Mapped[str] = mapped_column(
        String(3),
        default="INR",
        nullable=False,
    )

    status: Mapped[BookingStatus] = mapped_column(
        SAEnum(
            BookingStatus,
            name="booking_status",
            native_enum=True,
        ),
        default=BookingStatus.PENDING,
        nullable=False,
    )

    customer_notes: Mapped[str | None] = mapped_column(Text)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    customer: Mapped["User"] = relationship(
        back_populates="customer_bookings",
        foreign_keys=[customer_id],
    )

    organization: Mapped["ProviderOrganization"] = relationship(
        back_populates="bookings",
    )

    service: Mapped["Service"] = relationship(
        back_populates="bookings",
    )

    location: Mapped["BookingLocation | None"] = relationship(
        back_populates="booking",
        uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    assignments: Mapped[list["BookingAssignment"]] = relationship(
        back_populates="booking",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    status_history: Mapped[list["BookingStatusHistory"]] = relationship(
        back_populates="booking",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    travel: Mapped["BookingTravel | None"] = relationship(
        back_populates="booking",
        uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    payment: Mapped["Payment | None"] = relationship(
        back_populates="booking",
        uselist=False,
    )

    invoice: Mapped["Invoice | None"] = relationship(
        back_populates="booking",
        uselist=False,
    )

    review: Mapped["Review | None"] = relationship(
        back_populates="booking",
        uselist=False,
    )

    service_issues: Mapped[list["ServiceIssue"]] = relationship(
        back_populates="booking",
    )

    disputes: Mapped[list["Dispute"]] = relationship(
        back_populates="booking",
    )

    __table_args__ = (
        Index("ix_bookings_customer_id", "customer_id"),
        Index("ix_bookings_organization_id", "organization_id"),
        Index("ix_bookings_service_id", "service_id"),
        Index("ix_bookings_status", "status"),
        Index("ix_bookings_scheduled_start", "scheduled_start"),
        Index(
            "ix_bookings_org_schedule",
            "organization_id",
            "scheduled_start",
        ),
    )
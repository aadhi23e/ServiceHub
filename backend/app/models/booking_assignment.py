from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import DateTime, ForeignKey, Index, String, func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Enum as SAEnum

from app.enums.servicehub import AssignmentStatus

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.booking import Booking
    from app.models.provider_membership import ProviderMembership


class BookingAssignment(Base):
    __tablename__ = "booking_assignments"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    booking_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("bookings.id", ondelete="CASCADE"),
        nullable=False,
    )

    agent_membership_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("provider_memberships.id", ondelete="RESTRICT"),
        nullable=False,
    )

    reassigned_from_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey(
            "booking_assignments.id",
            ondelete="SET NULL",
        ),
    )

    status: Mapped[AssignmentStatus] = mapped_column(
        SAEnum(
            AssignmentStatus,
            name="assignment_status",
            native_enum=True,
        ),
        default=AssignmentStatus.ASSIGNED,
        nullable=False,
    )

    assignment_note: Mapped[str | None] = mapped_column(
        String(500),
    )

    assigned_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    accepted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
    )

    started_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
    )

    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
    )

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

    booking: Mapped["Booking"] = relationship(
        back_populates="assignments",
    )

    agent_membership: Mapped["ProviderMembership"] = relationship(
        back_populates="booking_assignments",
        foreign_keys=[agent_membership_id],
    )

    reassigned_from: Mapped["BookingAssignment | None"] = relationship(
        remote_side="BookingAssignment.id",
        foreign_keys=[reassigned_from_id],
    )

    __table_args__ = (
        Index(
            "ix_booking_assignments_booking_id",
            "booking_id",
        ),
        Index(
            "ix_booking_assignments_agent_membership_id",
            "agent_membership_id",
        ),
        Index(
            "ix_booking_assignments_status",
            "status",
        ),
    )
from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import DateTime, ForeignKey, Index, String, Text, func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Enum as SAEnum

from app.enums.servicehub import DisputeStatus
from app.db.base import Base

if TYPE_CHECKING:
    from app.models.booking import Booking
    from app.models.user import User


class Dispute(Base):
    __tablename__ = "disputes"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    booking_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("bookings.id", ondelete="RESTRICT"),
        nullable=False,
    )

    raised_by: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False,
    )

    reason: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    status: Mapped[DisputeStatus] = mapped_column(
        SAEnum(
            DisputeStatus,
            name="dispute_status",
            native_enum=True,
        ),
        default=DisputeStatus.OPEN,
        nullable=False,
    )

    resolution_notes: Mapped[str | None] = mapped_column(
        Text,
    )

    resolved_at: Mapped[datetime | None] = mapped_column(
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
        back_populates="disputes",
    )

    raised_by_user: Mapped["User"] = relationship(
        back_populates="disputes",
        foreign_keys=[raised_by],
    )

    __table_args__ = (
        Index("ix_disputes_booking_id", "booking_id"),
        Index("ix_disputes_raised_by", "raised_by"),
        Index("ix_disputes_status", "status"),
    )
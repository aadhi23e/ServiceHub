from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import DateTime, ForeignKey, Index, String, Text, func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Enum as SAEnum

from app.enums.servicehub import ServiceIssueStatus
from app.db.base import Base

if TYPE_CHECKING:
    from app.models.booking import Booking
    from app.models.user import User


class ServiceIssue(Base):
    __tablename__ = "service_issues"

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

    customer_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False,
    )

    title: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    status: Mapped[ServiceIssueStatus] = mapped_column(
        SAEnum(
            ServiceIssueStatus,
            name="service_issue_status",
            native_enum=True,
        ),
        default=ServiceIssueStatus.OPEN,
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
        back_populates="service_issues",
    )

    customer: Mapped["User"] = relationship(
        back_populates="service_issues",
    )

    __table_args__ = (
        Index(
            "ix_service_issues_booking_id",
            "booking_id",
        ),
        Index(
            "ix_service_issues_customer_id",
            "customer_id",
        ),
        Index(
            "ix_service_issues_status",
            "status",
        ),
    )
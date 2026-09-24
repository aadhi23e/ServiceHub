from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    BigInteger,
    CheckConstraint,
    DateTime,
    ForeignKey,
    ForeignKeyConstraint,
    Index,
    String,
    Text,
    text,
)
from sqlalchemy.dialects.postgresql import ExcludeConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.provider import ProviderProfile
    from app.models.review import Review
    from app.models.service import Service
    from app.models.user import User


class Booking(Base):
    __tablename__ = "bookings"

    __table_args__ = (
        CheckConstraint(
            "start_at < end_at",
            name="ck_bookings_time_range",
        ),
        CheckConstraint(
            "status IN ("
            "'PENDING', "
            "'CONFIRMED', "
            "'REJECTED', "
            "'CANCELLED', "
            "'IN_PROGRESS', "
            "'COMPLETED'"
            ")",
            name="ck_bookings_status",
        ),
        ForeignKeyConstraint(
            ["provider_id", "service_id"],
            ["services.provider_id", "services.id"],
            name="fk_bookings_provider_service",
            ondelete="RESTRICT",
        ),
        Index(
            "ix_bookings_customer_created",
            "customer_id",
            "created_at",
        ),
        Index(
            "ix_bookings_provider_start",
            "provider_id",
            "start_at",
        ),
        Index(
            "ix_bookings_provider_status",
            "provider_id",
            "status",
        ),
        Index(
            "ix_bookings_service_id",
            "service_id",
        ),
        Index(
            "ix_bookings_start_at",
            "start_at",
        ),
        Index(
            "ix_bookings_active_provider_start",
            "provider_id",
            "start_at",
            postgresql_where=text("status IN ('PENDING', 'CONFIRMED', 'IN_PROGRESS')"),
        ),
        ExcludeConstraint(
            (
                "provider_id",
                "=",
            ),
            (
                text("tstzrange(start_at, end_at, '[)')"),
                "&&",
            ),
            name="no_provider_overlapping_bookings",
            where=text("status IN ('PENDING', 'CONFIRMED', 'IN_PROGRESS')"),
            using="gist",
        ),
    )

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    customer_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey(
            "users.id",
            ondelete="RESTRICT",
        ),
        nullable=False,
    )

    provider_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey(
            "provider_profiles.id",
            ondelete="RESTRICT",
        ),
        nullable=False,
    )

    service_id: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
    )

    start_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    end_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="PENDING",
        server_default=text("'PENDING'"),
    )

    customer_notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    provider_notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=datetime.utcnow,
    )

    cancelled_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    customer: Mapped["User"] = relationship(
        back_populates="customer_bookings",
        foreign_keys=[customer_id],
    )

    provider: Mapped["ProviderProfile"] = relationship(
        back_populates="bookings",
        foreign_keys=[provider_id],
    )

    service: Mapped["Service"] = relationship(
        back_populates="bookings",
        primaryjoin="and_("
        "Booking.provider_id == Service.provider_id, "
        "Booking.service_id == Service.id"
        ")",
        foreign_keys=[provider_id, service_id],
    )

    review: Mapped["Review | None"] = relationship(
        back_populates="booking",
        uselist=False,
    )

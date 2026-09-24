from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    BigInteger,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    String,
    Text,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.availability import Availability
    from app.models.booking import Booking
    from app.models.review import Review
    from app.models.service import Service
    from app.models.user import User


class ProviderProfile(Base):
    __tablename__ = "provider_profiles"

    __table_args__ = (
        CheckConstraint(
            "status IN ('ACTIVE', 'SUSPENDED')",
            name="ck_provider_profiles_status",
        ),
        Index(
            "ix_provider_profiles_status",
            "status",
        ),
    )

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey(
            "users.id",
            ondelete="RESTRICT",
        ),
        unique=True,
        nullable=False,
    )

    business_name: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    phone: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True,
    )

    address: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    city: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="ACTIVE",
        server_default=text("'ACTIVE'"),
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

    timezone: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        default="Asia/Kolkata",
        server_default=text("'Asia/Kolkata'"),
    )

    user: Mapped["User"] = relationship(
        back_populates="provider_profile",
    )

    services: Mapped[list["Service"]] = relationship(
        back_populates="provider",
    )

    availability: Mapped[list["Availability"]] = relationship(
        back_populates="provider",
    )

    bookings: Mapped[list["Booking"]] = relationship(
        back_populates="provider",
    )

    reviews: Mapped[list["Review"]] = relationship(
        back_populates="provider",
    )

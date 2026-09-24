from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import (
    BigInteger,
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.booking import Booking
    from app.models.service_category import ServiceCategory
    from app.models.provider import ProviderProfile


class Service(Base):
    __tablename__ = "services"

    __table_args__ = (
        UniqueConstraint(
            "provider_id",
            "id",
            name="uq_services_provider_id_id",
        ),
        CheckConstraint(
            "duration_minutes > 0",
            name="ck_services_duration_positive",
        ),
        CheckConstraint(
            "price >= 0",
            name="ck_services_price_non_negative",
        ),
        Index(
            "ix_services_provider_id",
            "provider_id",
        ),
        Index(
            "ix_services_category_id",
            "category_id",
        ),
        Index(
            "ix_services_provider_active",
            "provider_id",
            "is_active",
        ),
        Index(
            "ix_services_category_active",
            "category_id",
            "is_active",
        ),
    )

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    provider_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey(
            "provider_profiles.id",
            ondelete="RESTRICT",
        ),
        nullable=False,
    )

    category_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey(
            "service_categories.id",
            ondelete="RESTRICT",
        ),
        nullable=False,
    )

    name: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    duration_minutes: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default=text("TRUE"),
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

    provider: Mapped["ProviderProfile"] = relationship(
        back_populates="services",
    )

    category: Mapped["ServiceCategory"] = relationship(
        back_populates="services",
    )

    bookings: Mapped[list["Booking"]] = relationship(
        back_populates="service",
    )

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import (
    ARRAY,
    Boolean,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    String,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Enum as SAEnum

from app.enums.servicehub import ServiceMode, ServiceStatus
from app.db.base import Base

if TYPE_CHECKING:
    from app.models.booking import Booking
    from app.models.provider_organization import ProviderOrganization
    from app.models.service_category import ServiceCategory
    from app.models.service_requirement import ServiceRequirement


class Service(Base):
    __tablename__ = "services"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    organization_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("provider_organizations.id", ondelete="RESTRICT"),
        nullable=False,
    )

    category_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("service_categories.id", ondelete="RESTRICT"),
        nullable=False,
    )

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(Text)

    price: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    currency: Mapped[str] = mapped_column(
        String(3),
        default="INR",
        nullable=False,
    )

    duration_minutes: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    buffer_minutes: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    status: Mapped[ServiceStatus] = mapped_column(
        SAEnum(
            ServiceStatus,
            name="service_status",
            native_enum=True,
        ),
        default=ServiceStatus.DRAFT,
        nullable=False,
    )

    service_modes: Mapped[list[str]] = mapped_column(
        ARRAY(
            SAEnum(
                ServiceMode,
                name="service_mode",
                native_enum=True,
            )
        ),
        nullable=False,
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

    organization: Mapped["ProviderOrganization"] = relationship(
        back_populates="services",
    )

    category: Mapped["ServiceCategory"] = relationship(
        back_populates="services",
    )

    requirements: Mapped[list["ServiceRequirement"]] = relationship(
        back_populates="service",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    bookings: Mapped[list["Booking"]] = relationship(
        back_populates="service",
    )

    __table_args__ = (
        Index(
            "ix_services_organization_id",
            "organization_id",
        ),
        Index(
            "ix_services_category_id",
            "category_id",
        ),
        Index(
            "ix_services_status",
            "status",
        ),
    )
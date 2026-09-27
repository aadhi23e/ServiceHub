from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import DateTime, ForeignKey, Index, String, Text, func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Enum as SAEnum

from app.enums.servicehub import ProviderLocationType
from app.db.base import Base

if TYPE_CHECKING:
    from app.models.address import Address
    from app.models.provider_organization import ProviderOrganization


class ProviderLocation(Base):
    __tablename__ = "provider_locations"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    organization_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("provider_organizations.id", ondelete="CASCADE"),
        nullable=False,
    )

    address_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("addresses.id", ondelete="RESTRICT"),
        nullable=False,
    )

    name: Mapped[str] = mapped_column(String(150), nullable=False)

    location_type: Mapped[ProviderLocationType] = mapped_column(
        SAEnum(
            ProviderLocationType,
            name="provider_location_type",
            native_enum=True,
        ),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(Text)

    is_active: Mapped[bool] = mapped_column(
        default=True,
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
        back_populates="locations",
    )

    address: Mapped["Address"] = relationship()

    __table_args__ = (
        Index("ix_provider_locations_organization_id", "organization_id"),
        Index("ix_provider_locations_address_id", "address_id"),
        Index("ix_provider_locations_location_type", "location_type"),
    )
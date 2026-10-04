from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    Numeric,
    String,
    UniqueConstraint,
    text,
)
from sqlalchemy.dialects.postgresql import ARRAY, UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.provider_organization import ProviderOrganization
    from app.models.provider_service_member import ProviderServiceMember
    from app.models.service import Service


class ProviderServiceOffering(Base):
    __tablename__ = "provider_service_offerings"

    __table_args__ = (
        UniqueConstraint(
            "organization_id",
            "service_id",
            name="uq_provider_service_offerings_organization_service",
        ),
        CheckConstraint(
            "price >= 0",
            name="ck_provider_service_offerings_price_non_negative",
        ),
        CheckConstraint(
            "duration_minutes > 0",
            name="ck_provider_service_offerings_duration_positive",
        ),
        CheckConstraint(
            "buffer_minutes >= 0",
            name="ck_provider_service_offerings_buffer_non_negative",
        ),
        CheckConstraint(
            "array_length(service_modes, 1) >= 1",
            name="ck_provider_service_offerings_service_modes_not_empty",
        ),
        Index(
            "ix_provider_service_offerings_organization_id",
            "organization_id",
        ),
        Index(
            "ix_provider_service_offerings_service_id",
            "service_id",
        ),
        Index(
            "ix_provider_service_offerings_is_active",
            "is_active",
        ),
    )

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    organization_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey(
            "provider_organizations.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    service_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey(
            "services.id",
            ondelete="RESTRICT",
        ),
        nullable=False,
    )

    price: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    currency: Mapped[str] = mapped_column(
        String(3),
        nullable=False,
        default="INR",
        server_default="INR",
    )

    duration_minutes: Mapped[int] = mapped_column(
        nullable=False,
    )

    buffer_minutes: Mapped[int] = mapped_column(
        nullable=False,
        default=0,
        server_default="0",
    )

    service_modes: Mapped[list[str]] = mapped_column(
        ARRAY(String(50)),
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default=text("true"),
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

    organization: Mapped["ProviderOrganization"] = relationship(
        back_populates="service_offerings",
        foreign_keys=[organization_id],
    )

    service: Mapped["Service"] = relationship(
        back_populates="provider_offerings",
        foreign_keys=[service_id],
    )

    members: Mapped[list["ProviderServiceMember"]] = relationship(
        back_populates="service_offering",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
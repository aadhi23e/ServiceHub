from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import (
    Boolean,
    DateTime,
    Enum,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
    text,
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.enums.servicehub import ServiceRequirementType

if TYPE_CHECKING:
    from app.models.service import Service


class ServiceRequirement(Base):
    """
    House Cleaning
    ├── number_of_rooms     NUMBER     required
    ├── cleaning_type       SELECT     required
    └── has_pets            BOOLEAN    optional
    """
    __tablename__ = "service_requirements"

    __table_args__ = (
        UniqueConstraint(
            "service_id",
            "key",
            name="uq_service_requirements_service_key",
        ),
        Index(
            "ix_service_requirements_service_id",
            "service_id",
        ),
        Index(
            "ix_service_requirements_is_active",
            "is_active",
        ),
    )

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    service_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey(
            "services.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    key: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    label: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    requirement_type: Mapped[ServiceRequirementType] = mapped_column(
        Enum(
            ServiceRequirementType,
            name="service_requirement_type",
        ),
        nullable=False,
    )

    is_required: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        server_default=text("false"),
    )

    sort_order: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        server_default=text("0"),
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
    )

    service: Mapped["Service"] = relationship(
        back_populates="requirements",
        foreign_keys=[service_id],
    )
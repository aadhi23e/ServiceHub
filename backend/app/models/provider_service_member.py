from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Index,
    UniqueConstraint,
    text,
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.provider_membership import ProviderMembership
    from app.models.provider_service_offering import ProviderServiceOffering


class ProviderServiceMember(Base):
    __tablename__ = "provider_service_members"

    __table_args__ = (
        UniqueConstraint(
            "provider_service_offering_id",
            "provider_membership_id",
            name="uq_provider_service_member_offering_membership",
        ),
        Index(
            "ix_provider_service_members_offering_id",
            "provider_service_offering_id",
        ),
        Index(
            "ix_provider_service_members_membership_id",
            "provider_membership_id",
        ),
        Index(
            "ix_provider_service_members_is_active",
            "is_active",
        ),
    )

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    provider_service_offering_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey(
            "provider_service_offerings.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    provider_membership_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey(
            "provider_memberships.id",
            ondelete="CASCADE",
        ),
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

    service_offering: Mapped["ProviderServiceOffering"] = relationship(
        back_populates="members",
        foreign_keys=[provider_service_offering_id],
    )

    provider_membership: Mapped["ProviderMembership"] = relationship(
        back_populates="service_assignments",
        foreign_keys=[provider_membership_id],
    )
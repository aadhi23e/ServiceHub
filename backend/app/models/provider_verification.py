from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Index,
    String,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.enums.servicehub import VerificationStatus

if TYPE_CHECKING:
    from app.models.provider_organization import ProviderOrganization
    from app.models.user import User


class ProviderVerification(Base):
    __tablename__ = "provider_verifications"

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

    reviewed_by: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey(
            "users.id",
            ondelete="SET NULL",
        ),
        nullable=True,
    )

    status: Mapped[VerificationStatus] = mapped_column(
        SAEnum(
            VerificationStatus,
            name="verification_status",
            native_enum=True,
        ),
        default=VerificationStatus.PENDING,
        nullable=False,
    )

    document_reference: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    rejection_reason: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    reviewed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    expires_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
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
        back_populates="verifications",
    )

    reviewed_by_user: Mapped["User | None"] = relationship(
        back_populates="reviewed_provider_verifications",
        foreign_keys=[reviewed_by],
    )

    __table_args__ = (
        Index(
            "ix_provider_verifications_organization_id",
            "organization_id",
        ),
        Index(
            "ix_provider_verifications_status",
            "status",
        ),
        Index(
            "ix_provider_verifications_reviewed_by",
            "reviewed_by",
        ),
    )
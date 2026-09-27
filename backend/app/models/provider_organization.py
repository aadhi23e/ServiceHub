from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import (
    DateTime,
    Enum,
    ForeignKey,
    Index,
    String,
    Text,
    text,
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.enums.provider import ProviderStatus

if TYPE_CHECKING:
    from app.models.provider_membership import ProviderMembership
    from app.models.user import User


class ProviderOrganization(Base):
    __tablename__ = "provider_organizations"

    __table_args__ = (
        Index(
            "ix_provider_organizations_status",
            "status",
        ),
        Index(
            "ix_provider_organizations_created_by",
            "created_by",
        ),
        Index(
            "ix_provider_organizations_name",
            "name",
        ),
    )

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    # ------------------------------------------------------------------
    # Organization identity
    # ------------------------------------------------------------------

    name: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    legal_name: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    status: Mapped[ProviderStatus] = mapped_column(
        Enum(
            ProviderStatus,
            name="provider_status",
        ),
        nullable=False,
        default=ProviderStatus.PENDING,
        server_default=ProviderStatus.PENDING.value,
    )

    # ------------------------------------------------------------------
    # Audit ownership
    # ------------------------------------------------------------------

    created_by: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey(
            "users.id",
            ondelete="RESTRICT",
        ),
        nullable=False,
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

    # ------------------------------------------------------------------
    # Relationships
    # ------------------------------------------------------------------

    created_by_user: Mapped["User"] = relationship(
        back_populates="created_provider_organizations",
        foreign_keys=[created_by],
    )

    memberships: Mapped[list["ProviderMembership"]] = relationship(
        back_populates="organization",
        foreign_keys="ProviderMembership.organization_id",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
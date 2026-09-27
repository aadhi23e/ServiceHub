from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import DateTime, ForeignKey, Index, JSON, String, func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.user import User


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    actor_user_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
    )

    action: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    resource_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    resource_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
    )

    request_id: Mapped[str | None] = mapped_column(
        String(100),
    )

    track_id: Mapped[str | None] = mapped_column(
        String(100),
    )

    metadata_JSON: Mapped[dict | None] = mapped_column(
        "metadata",
        JSON,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    actor: Mapped["User | None"] = relationship(
        back_populates="audit_logs",
        foreign_keys=[actor_user_id],
    )

    __table_args__ = (
        Index(
            "ix_audit_logs_actor_user_id",
            "actor_user_id",
        ),
        Index(
            "ix_audit_logs_resource",
            "resource_type",
            "resource_id",
        ),
        Index(
            "ix_audit_logs_request_id",
            "request_id",
        ),
        Index(
            "ix_audit_logs_track_id",
            "track_id",
        ),
        Index(
            "ix_audit_logs_created_at",
            "created_at",
        ),
    )
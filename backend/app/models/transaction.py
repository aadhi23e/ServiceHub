from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import DateTime, ForeignKey, Index, Numeric, String, func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Enum as SAEnum

from app.enums.servicehub import TransactionType
from app.db.base import Base

if TYPE_CHECKING:
    from app.models.payment import Payment
    from app.models.provider_organization import ProviderOrganization


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    payment_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("payments.id", ondelete="SET NULL"),
    )

    organization_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("provider_organizations.id", ondelete="RESTRICT"),
        nullable=False,
    )

    transaction_type: Mapped[TransactionType] = mapped_column(
        SAEnum(
            TransactionType,
            name="transaction_type",
            native_enum=True,
        ),
        nullable=False,
    )

    amount: Mapped[Decimal] = mapped_column(
        Numeric(14, 2),
        nullable=False,
    )

    currency: Mapped[str] = mapped_column(
        String(3),
        default="INR",
        nullable=False,
    )

    reference: Mapped[str | None] = mapped_column(
        String(255),
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    payment: Mapped["Payment | None"] = relationship(
        back_populates="transactions",
    )

    organization: Mapped["ProviderOrganization"] = relationship()

    __table_args__ = (
        Index("ix_transactions_payment_id", "payment_id"),
        Index(
            "ix_transactions_organization_id",
            "organization_id",
        ),
        Index(
            "ix_transactions_transaction_type",
            "transaction_type",
        ),
        Index("ix_transactions_created_at", "created_at"),
    )
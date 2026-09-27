from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import DateTime, Index, Numeric, String, text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.user_address import UserAddress


class Address(Base):
    __tablename__ = "addresses"

    __table_args__ = (
        Index("ix_addresses_postal_code", "postal_code"),
        Index("ix_addresses_city", "city"),
        Index("ix_addresses_state", "state"),
    )

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True),primary_key=True,default=uuid4,)

    # ------------------------------------------------------------------
    # Address
    # ------------------------------------------------------------------

    address_line_1: Mapped[str] = mapped_column(String(255),nullable=False,)

    address_line_2: Mapped[str | None] = mapped_column(String(255),nullable=True,)

    landmark: Mapped[str | None] = mapped_column(String(255),nullable=True,)

    city: Mapped[str] = mapped_column(String(100),nullable=False,)

    state: Mapped[str] = mapped_column(String(100),nullable=False,)

    postal_code: Mapped[str] = mapped_column(String(20),nullable=False,)

    country_code: Mapped[str] = mapped_column(String(2),nullable=False,server_default="IN",)

    # ------------------------------------------------------------------
    # Optional geographic coordinates
    # ------------------------------------------------------------------

    latitude: Mapped[float | None] = mapped_column(Numeric(9, 6),nullable=True,)

    longitude: Mapped[float | None] = mapped_column(Numeric(9, 6),nullable=True,)

    # ------------------------------------------------------------------
    # Timestamps
    # ------------------------------------------------------------------

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),nullable=False,server_default=text("CURRENT_TIMESTAMP"),)

    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),nullable=False,server_default=text("CURRENT_TIMESTAMP"),onupdate=datetime.utcnow,)

    # ------------------------------------------------------------------
    # Customer associations
    # ------------------------------------------------------------------

    user_addresses: Mapped[list["UserAddress"]] = relationship(back_populates="address",foreign_keys="UserAddress.address_id",)
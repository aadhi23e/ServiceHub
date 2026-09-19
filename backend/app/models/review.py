from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    BigInteger,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    SmallInteger,
    Text,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.booking import Booking
    from app.models.provider import ProviderProfile
    from app.models.user import User

class Review(Base):
    __tablename__ = "reviews"

    __table_args__ = (
        CheckConstraint(
            "rating >= 1 AND rating <= 5",
            name="ck_reviews_rating",
        ),
        Index(
            "ix_reviews_customer_id",
            "customer_id",
        ),
        Index(
            "ix_reviews_provider_id",
            "provider_id",
        ),
        Index(
            "ix_reviews_created_at",
            "created_at",
        ),
    )

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    booking_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey(
            "bookings.id",
            ondelete="RESTRICT",
        ),
        unique=True,
        nullable=False,
    )

    customer_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey(
            "users.id",
            ondelete="RESTRICT",
        ),
        nullable=False,
    )

    provider_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey(
            "provider_profiles.id",
            ondelete="RESTRICT",
        ),
        nullable=False,
    )

    rating: Mapped[int] = mapped_column(
        SmallInteger,
        nullable=False,
    )

    comment: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
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

    booking: Mapped["Booking"] = relationship(
        back_populates="review",
    )

    customer: Mapped["User"] = relationship(
        back_populates="reviews",
        foreign_keys=[customer_id],
    )

    provider: Mapped["ProviderProfile"] = relationship(
        back_populates="reviews",
        foreign_keys=[provider_id],
    )
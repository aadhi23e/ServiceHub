from datetime import time
from typing import TYPE_CHECKING

from sqlalchemy import (
    BigInteger,
    Boolean,
    CheckConstraint,
    ForeignKey,
    Index,
    SmallInteger,
    Time,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.provider import ProviderProfile


class Availability(Base):
    __tablename__ = "availability"

    __table_args__ = (
        CheckConstraint(
            "day_of_week >= 0 AND day_of_week <= 6",
            name="ck_availability_day_of_week",
        ),
        CheckConstraint(
            "start_time < end_time",
            name="ck_availability_time_range",
        ),
        Index(
            "ix_availability_provider_day",
            "provider_id",
            "day_of_week",
        ),
        Index(
            "ix_availability_provider_active",
            "provider_id",
            "is_active",
        ),
    )

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    provider_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey(
            "provider_profiles.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    day_of_week: Mapped[int] = mapped_column(
        SmallInteger,
        nullable=False,
    )

    start_time: Mapped[time] = mapped_column(
        Time,
        nullable=False,
    )

    end_time: Mapped[time] = mapped_column(
        Time,
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default=text("TRUE"),
    )

    provider: Mapped["ProviderProfile"] = relationship(
        back_populates="availability",
    )

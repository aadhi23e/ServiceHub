from datetime import datetime

from sqlalchemy import BigInteger, CheckConstraint, DateTime, Index, String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.audit_log import AuditLog
    from app.models.booking import Booking
    from app.models.notification import Notification
    from app.models.provider import ProviderProfile
    from app.models.review import Review
    
class User(Base):
    __tablename__ = "users"

    __table_args__ = (
        CheckConstraint(
            "role IN ('CUSTOMER', 'PROVIDER', 'ADMIN')",
            name="ck_users_role",
        ),
        CheckConstraint(
            "status IN ('ACTIVE', 'SUSPENDED')",
            name="ck_users_status",
        ),
        Index("ix_users_role", "role"),
        Index("ix_users_status", "status"),
        Index("ix_users_created_at", "created_at"),
    )

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    first_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    last_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    phone: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True,
    )

    role: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="ACTIVE",
        server_default=text("'ACTIVE'"),
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

    last_login_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    provider_profile: Mapped["ProviderProfile | None"] = relationship(
        back_populates="user",
        uselist=False,
    )

    customer_bookings: Mapped[list["Booking"]] = relationship(
        back_populates="customer",
        foreign_keys="Booking.customer_id",
    )

    reviews: Mapped[list["Review"]] = relationship(
        back_populates="customer",
        foreign_keys="Review.customer_id",
    )

    notifications: Mapped[list["Notification"]] = relationship(
        back_populates="user",
    )

    audit_logs: Mapped[list["AuditLog"]] = relationship(
        back_populates="actor",
    )
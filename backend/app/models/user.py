from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import Boolean, DateTime, Enum, Index, String, text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.enums.user import UserRole, UserStatus

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.address import Address
    from app.models.audit_log import AuditLog
    from app.models.booking import Booking
    from app.models.dispute import Dispute
    from app.models.notification import Notification
    from app.models.provider_membership import ProviderMembership
    from app.models.provider_organization import ProviderOrganization
    from app.models.provider_profile import ProviderProfile
    from app.models.provider_verification import ProviderVerification
    from app.models.review import Review
    from app.models.service_issue import ServiceIssue
    from app.models.user_address import UserAddress


class User(Base):
    __tablename__ = "users"

    __table_args__ = (
        Index("ix_users_role", "role"),
        Index("ix_users_status", "status"),
        Index("ix_users_phone", "phone"),
        Index("ix_users_created_at", "created_at"),
    )

    # ------------------------------------------------------------------
    # Identity
    # ------------------------------------------------------------------

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True),primary_key=True,default=uuid4,)
    email: Mapped[str] = mapped_column(String(255),unique=True,nullable=False,)
    password_hash: Mapped[str] = mapped_column(String(255),nullable=False,)
    first_name: Mapped[str] = mapped_column(String(100),nullable=False,)
    last_name: Mapped[str | None] = mapped_column(String(100),nullable=True,)
    phone: Mapped[str | None] = mapped_column(String(20),nullable=True,)

    # ------------------------------------------------------------------
    # Platform role / account status
    # ------------------------------------------------------------------

    role: Mapped[UserRole] = mapped_column(Enum(UserRole, name="user_role"),nullable=False,default=UserRole.CUSTOMER,server_default=UserRole.CUSTOMER.value,)
    status: Mapped[UserStatus] = mapped_column(Enum(UserStatus, name="user_status"),nullable=False,default=UserStatus.ACTIVE,server_default=UserStatus.ACTIVE.value,)

    # ------------------------------------------------------------------
    # Observability
    # ------------------------------------------------------------------

    last_login_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True),nullable=True,)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),nullable=False,server_default=text("CURRENT_TIMESTAMP"),)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),nullable=False,server_default=text("CURRENT_TIMESTAMP"),onupdate=datetime.utcnow,)

    # ------------------------------------------------------------------
    # Customer addresses
    # ------------------------------------------------------------------

    addresses: Mapped[list["UserAddress"]] = relationship(back_populates="user",foreign_keys="UserAddress.user_id",cascade="all, delete-orphan",passive_deletes=True,)

    # ------------------------------------------------------------------
    # Provider profile
    # ------------------------------------------------------------------

    provider_profile: Mapped["ProviderProfile | None"] = relationship(back_populates="user",foreign_keys="ProviderProfile.user_id",uselist=False,cascade="all, delete-orphan",passive_deletes=True,)

    # ------------------------------------------------------------------
    # Provider memberships
    # ------------------------------------------------------------------

    provider_memberships: Mapped[list["ProviderMembership"]] = relationship(back_populates="user",foreign_keys="ProviderMembership.user_id",cascade="all, delete-orphan",passive_deletes=True,)

    # ------------------------------------------------------------------
    # Organizations created by this user
    # ------------------------------------------------------------------

    created_provider_organizations: Mapped[list["ProviderOrganization"]
    ] = relationship(back_populates="created_by_user",foreign_keys="ProviderOrganization.created_by",)

    # ------------------------------------------------------------------
    # Customer relationships
    # ------------------------------------------------------------------

    customer_bookings: Mapped[list["Booking"]] = relationship(back_populates="customer",foreign_keys="Booking.customer_id",)
    reviews: Mapped[list["Review"]] = relationship(back_populates="customer",foreign_keys="Review.customer_id",)
    service_issues: Mapped[list["ServiceIssue"]] = relationship(
        back_populates="customer",
        foreign_keys="ServiceIssue.customer_id",
    )
    disputes: Mapped[list["Dispute"]] = relationship(
        back_populates="raised_by_user",
        foreign_keys="Dispute.raised_by",
    )
    # ------------------------------------------------------------------
    # Notifications / audit
    # ------------------------------------------------------------------

    notifications: Mapped[list["Notification"]] = relationship(back_populates="user",foreign_keys="Notification.user_id",)
    audit_logs: Mapped[list["AuditLog"]] = relationship(back_populates="actor",foreign_keys="AuditLog.actor_user_id",)

    # ------------------------------------------------------------------
    # Provider verification
    # ------------------------------------------------------------------

    reviewed_provider_verifications: Mapped[list["ProviderVerification"]] = relationship(back_populates="reviewed_by_user",foreign_keys="ProviderVerification.reviewed_by",)
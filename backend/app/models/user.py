from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import Boolean, DateTime, Index, String, text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.enums.user import UserStatus

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.audit_log import AuditLog
    from app.models.booking import Booking
    from app.models.dispute import Dispute
    from app.models.notification import Notification
    from app.models.provider_membership import ProviderMembership
    from app.models.provider_organization import ProviderOrganization
    from app.models.provider_verification import ProviderVerification
    from app.models.review import Review
    from app.models.service_issue import ServiceIssue


class User(Base):
    __tablename__ = "users"

    __table_args__ = (
        Index("ix_users_status", "status"),
        Index("ix_users_phone", "phone"),
        Index("ix_users_created_at", "created_at"),
    )

    # Detial
    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True),primary_key=True,default=uuid4,)
    email: Mapped[str] = mapped_column(String(255),unique=True,nullable=False,)
    password_hash: Mapped[str] = mapped_column(String(255),nullable=False,)
    first_name: Mapped[str] = mapped_column(String(100),nullable=False,)
    last_name: Mapped[str | None] = mapped_column(String(100),nullable=True,)
    phone: Mapped[str | None] = mapped_column(String(20),nullable=True,)

    # Status
    status: Mapped[UserStatus] = mapped_column(String(20),nullable=False,default=UserStatus.ACTIVE,server_default=UserStatus.ACTIVE.value,)
    is_admin: Mapped[bool] = mapped_column(Boolean,nullable=False,default=False,server_default=text("false"),)

    # address: Mapped[list["location"]] = TODO: NEED to have a [address because the customer can have more address] same goes for orginzation same orginzation different location
    
    # observability.
    last_login_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True),nullable=True,)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),nullable=False,server_default=text("CURRENT_TIMESTAMP"),)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),nullable=False,server_default=text("CURRENT_TIMESTAMP"),onupdate=datetime.utcnow,)

    # ------------------------------------------------------------------
    # Provider organization memberships
    # ------------------------------------------------------------------

    provider_memberships: Mapped[list["ProviderMembership"]] = relationship(back_populates="user",foreign_keys="ProviderMembership.user_id",)

    # ------------------------------------------------------------------
    # Provider organizations created by this user
    # ------------------------------------------------------------------

    created_provider_organizations: Mapped[list["ProviderOrganization"]] = relationship(back_populates="created_by_user",foreign_keys="ProviderOrganization.created_by",)

    # ------------------------------------------------------------------
    # Customer relationships
    # ------------------------------------------------------------------

    customer_bookings: Mapped[list["Booking"]] = relationship(back_populates="customer",foreign_keys="Booking.customer_id",)
    reviews: Mapped[list["Review"]] = relationship(back_populates="customer",foreign_keys="Review.customer_id",)
    service_issues: Mapped[list["ServiceIssue"]] = relationship(back_populates="reported_by_user",foreign_keys="ServiceIssue.reported_by",)
    disputes: Mapped[list["Dispute"]] = relationship(back_populates="opened_by_user",foreign_keys="Dispute.opened_by",)

    # ------------------------------------------------------------------
    # Notifications / audit
    # ------------------------------------------------------------------

    notifications: Mapped[list["Notification"]] = relationship(back_populates="user",foreign_keys="Notification.user_id",)
    audit_logs: Mapped[list["AuditLog"]] = relationship(back_populates="actor",foreign_keys="AuditLog.actor_user_id",)

    # ------------------------------------------------------------------
    # Provider verification
    # ------------------------------------------------------------------

    provider_verifications: Mapped[list["ProviderVerification"]] = relationship(back_populates="reviewed_by_user",foreign_keys="ProviderVerification.reviewed_by",)

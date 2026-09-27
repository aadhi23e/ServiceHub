from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    Enum,
    ForeignKey,
    Index,
    text,
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.enums.provider import (
    AgentType,
    MembershipStatus,
    ProviderMembershipRole,
)

if TYPE_CHECKING:
    from app.models.provider_organization import ProviderOrganization
    from app.models.user import User
    from app.models.agent_availability import AgentAvailability
    from app.models.agent_time_off import AgentTimeOff
    from app.models.booking_assignment import BookingAssignment
class ProviderMembership(Base):
    __tablename__ = "provider_memberships"

    __table_args__ = (
        CheckConstraint(
            """
            (
                role = 'AGENT'
                AND agent_type IS NOT NULL
            )
            OR
            (
                role IN ('OWNER', 'MANAGER')
                AND agent_type IS NULL
            )
            """,
            name="ck_provider_memberships_agent_type_by_role",
        ),
        CheckConstraint(
            """
            (
                status = 'INVITED'
                AND joined_at IS NULL
            )
            OR
            status != 'INVITED'
            """,
            name="ck_provider_memberships_invitation_state",
        ),
        Index(
            "ix_provider_memberships_user_id",
            "user_id",
        ),
        Index(
            "ix_provider_memberships_organization_id",
            "organization_id",
        ),
        Index(
            "ix_provider_memberships_role",
            "role",
        ),
        Index(
            "ix_provider_memberships_status",
            "status",
        ),
    )

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    # ------------------------------------------------------------------
    # Relationships / ownership
    # ------------------------------------------------------------------

    user_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    organization_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey(
            "provider_organizations.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    # ------------------------------------------------------------------
    # Organization authorization
    # ------------------------------------------------------------------

    role: Mapped[ProviderMembershipRole] = mapped_column(
        Enum(
            ProviderMembershipRole,
            name="provider_membership_role",
        ),
        nullable=False,
    )

    agent_type: Mapped[AgentType | None] = mapped_column(
        Enum(
            AgentType,
            name="agent_type",
        ),
        nullable=True,
    )

    status: Mapped[MembershipStatus] = mapped_column(
        Enum(
            MembershipStatus,
            name="membership_status",
        ),
        nullable=False,
        default=MembershipStatus.INVITED,
        server_default=MembershipStatus.INVITED.value,
    )

    # ------------------------------------------------------------------
    # Membership lifecycle
    # ------------------------------------------------------------------

    invited_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    joined_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    removed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
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

    # ------------------------------------------------------------------
    # Relationships
    # ------------------------------------------------------------------

    user: Mapped["User"] = relationship(
        back_populates="provider_memberships",
        foreign_keys=[user_id],
    )

    organization: Mapped["ProviderOrganization"] = relationship(
        back_populates="memberships",
        foreign_keys=[organization_id],
    )

    availabilities: Mapped[list["AgentAvailability"]] = relationship(
        back_populates="agent_membership",
        cascade="all, delete-orphan",
    )

    time_offs: Mapped[list["AgentTimeOff"]] = relationship(
        back_populates="agent_membership",
        cascade="all, delete-orphan",
    )

    booking_assignments: Mapped[list["BookingAssignment"]] = relationship(
        back_populates="agent_membership",
    )
    
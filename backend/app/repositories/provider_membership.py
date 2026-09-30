from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.enums.provider import (
    MembershipStatus,
    ProviderMembershipRole,
)
from app.models.provider_membership import ProviderMembership
from app.models.user import User


class ProviderMembershipRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(
        self,
        membership_id: UUID,
    ) -> ProviderMembership | None:

        statement = select(
            ProviderMembership
        ).where(
            ProviderMembership.id == membership_id,
        )

        return self.db.scalar(statement)

    def get_active_by_user_and_org(
        self,
        *,
        user_id: UUID,
        organization_id: UUID,
    ) -> ProviderMembership | None:

        statement = select(
            ProviderMembership
        ).where(
            ProviderMembership.user_id == user_id,
            ProviderMembership.organization_id == organization_id,
            ProviderMembership.status
            == MembershipStatus.ACTIVE,
        )

        return self.db.scalar(statement)

    def get_any_by_user_and_org(
        self,
        *,
        user_id: UUID,
        organization_id: UUID,
    ) -> ProviderMembership | None:

        statement = select(
            ProviderMembership
        ).where(
            ProviderMembership.user_id == user_id,
            ProviderMembership.organization_id == organization_id,
        )

        return self.db.scalar(statement)

    def get_active_for_user(
        self,
        *,
        user_id: UUID,
    ) -> ProviderMembership | None:

        statement = (
            select(ProviderMembership)
            .where(
                ProviderMembership.user_id == user_id,
                ProviderMembership.status
                == MembershipStatus.ACTIVE,
            )
            .order_by(
                ProviderMembership.joined_at.asc()
            )
            .limit(1)
        )

        return self.db.scalar(statement)

    def list_organization(
        self,
        *,
        organization_id: UUID,
        page: int,
        page_size: int,
    ) -> tuple[list[ProviderMembership], int]:

        conditions = [
            ProviderMembership.organization_id
            == organization_id,
            ProviderMembership.status
            != MembershipStatus.REMOVED,
        ]

        count_statement = (
            select(func.count())
            .select_from(ProviderMembership)
            .where(*conditions)
        )

        total = int(
            self.db.scalar(count_statement) or 0
        )

        offset = (page - 1) * page_size

        statement = (
            select(ProviderMembership)
            .join(
                User,
                User.id == ProviderMembership.user_id,
            )
            .where(*conditions)
            .order_by(
                User.first_name.asc(),
                User.last_name.asc(),
            )
            .offset(offset)
            .limit(page_size)
        )

        members = list(
            self.db.scalars(statement).all()
        )

        return members, total

    def create(
        self,
        *,
        user_id: UUID,
        organization_id: UUID,
        role: ProviderMembershipRole,
        agent_type=None,
    ) -> ProviderMembership:

        membership = ProviderMembership(
            user_id=user_id,
            organization_id=organization_id,
            role=role,
            agent_type=agent_type,
            status=MembershipStatus.ACTIVE,
        )

        membership.joined_at = func.now()

        self.db.add(membership)
        self.db.flush()

        return membership

    def update(
        self,
        membership: ProviderMembership,
        *,
        role=None,
        agent_type=None,
    ) -> ProviderMembership:

        if role is not None:
            membership.role = role

        membership.agent_type = agent_type

        self.db.flush()

        return membership

    def remove(
        self,
        membership: ProviderMembership,
    ) -> ProviderMembership:

        membership.status = MembershipStatus.REMOVED
        membership.removed_at = func.now()

        self.db.flush()

        return membership
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.provider_service_member import ProviderServiceMember


class ProviderServiceMemberRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(
        self,
        *,
        member_id: UUID,
        offering_id: UUID,
    ) -> ProviderServiceMember | None:
        stmt = (
            select(ProviderServiceMember)
            .options(
                selectinload(
                    ProviderServiceMember.provider_membership,
                ).selectinload(
                    ProviderServiceMember.provider_membership.user,
                )
            )
            .where(
                ProviderServiceMember.id == member_id,
                ProviderServiceMember.provider_service_offering_id
                == offering_id,
            )
        )

        return self.db.scalar(stmt)

    def get_by_membership(
        self,
        *,
        offering_id: UUID,
        membership_id: UUID,
    ) -> ProviderServiceMember | None:
        stmt = (
            select(ProviderServiceMember)
            .options(
                selectinload(
                    ProviderServiceMember.provider_membership,
                ).selectinload(
                    ProviderServiceMember.provider_membership.user,
                )
            )
            .where(
                ProviderServiceMember.provider_service_offering_id
                == offering_id,
                ProviderServiceMember.provider_membership_id
                == membership_id,
            )
        )

        return self.db.scalar(stmt)

    def list_by_offering(
        self,
        *,
        offering_id: UUID,
    ) -> list[ProviderServiceMember]:
        stmt = (
            select(ProviderServiceMember)
            .options(
                selectinload(
                    ProviderServiceMember.provider_membership,
                ).selectinload(
                    ProviderServiceMember.provider_membership.user,
                )
            )
            .where(
                ProviderServiceMember.provider_service_offering_id
                == offering_id,
                ProviderServiceMember.is_active.is_(True),
            )
            .order_by(
                ProviderServiceMember.created_at.asc(),
            )
        )

        return list(self.db.scalars(stmt).all())

    def create(
        self,
        member: ProviderServiceMember,
    ) -> ProviderServiceMember:
        self.db.add(member)
        self.db.flush()
        self.db.refresh(member)

        return member

    def update(
        self,
        member: ProviderServiceMember,
    ) -> ProviderServiceMember:
        self.db.flush()
        self.db.refresh(member)

        return member
from uuid import UUID

from fastapi import HTTPException, status

from app.enums.provider import (
    MembershipStatus,
    ProviderMembershipRole,
)
from app.models.provider_service_member import ProviderServiceMember
from app.repositories.provider_membership import (
    ProviderMembershipRepository,
)
from app.repositories.provider_service_member import (
    ProviderServiceMemberRepository,
)
from app.repositories.provider_service_offering import (
    ProviderServiceOfferingRepository,
)
from app.schemas.provider_service_member import (
    ProviderServiceMemberCreateRequest,
)


class ProviderServiceMemberService:
    def __init__(
        self,
        *,
        db,
        member_repo: ProviderServiceMemberRepository,
        offering_repo: ProviderServiceOfferingRepository,
        membership_repo: ProviderMembershipRepository,
    ):
        self.db = db
        self.member_repo = member_repo
        self.offering_repo = offering_repo
        self.membership_repo = membership_repo

    def get_provider_membership(
        self,
        *,
        user_id: UUID,
    ):
        membership = (
            self.membership_repo.get_active_membership_for_user(
                user_id=user_id,
            )
        )

        if membership is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not an active provider member.",
            )

        return membership

    def require_manager(
        self,
        *,
        user_id: UUID,
    ):
        membership = self.get_provider_membership(
            user_id=user_id,
        )

        if membership.role not in {
            ProviderMembershipRole.OWNER,
            ProviderMembershipRole.MANAGER,
        }:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=(
                    "Only organization owners and managers "
                    "can manage service members."
                ),
            )

        return membership

    def get_offering_for_organization(
        self,
        *,
        offering_id: UUID,
        organization_id: UUID,
    ):
        offering = self.offering_repo.get_by_id(
            offering_id=offering_id,
            organization_id=organization_id,
        )

        if offering is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Service offering not found.",
            )

        return offering

    def list_members(
        self,
        *,
        user_id: UUID,
        offering_id: UUID,
    ):
        membership = self.get_provider_membership(
            user_id=user_id,
        )

        self.get_offering_for_organization(
            offering_id=offering_id,
            organization_id=membership.organization_id,
        )

        return self.member_repo.list_by_offering(
            offering_id=offering_id,
        )

    def assign_member(
        self,
        *,
        user_id: UUID,
        offering_id: UUID,
        payload: ProviderServiceMemberCreateRequest,
    ):
        manager_membership = self.require_manager(
            user_id=user_id,
        )

        offering = self.get_offering_for_organization(
            offering_id=offering_id,
            organization_id=manager_membership.organization_id,
        )

        if not offering.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot assign a member to an inactive service offering.",
            )

        target_membership = (
            self.membership_repo.get_by_id(
                payload.provider_membership_id,
            )
        )

        if target_membership is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Provider membership not found.",
            )

        if (
            target_membership.organization_id
            != manager_membership.organization_id
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="The provider membership does not belong to your organization.",
            )

        if target_membership.status != MembershipStatus.ACTIVE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only active provider members can be assigned.",
            )

        if target_membership.role != ProviderMembershipRole.AGENT:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only provider agents can be assigned to service offerings.",
            )

        existing = self.member_repo.get_by_membership(
            offering_id=offering.id,
            membership_id=target_membership.id,
        )

        if existing is not None:
            if existing.is_active:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="This agent is already assigned to the service offering.",
                )

            existing.is_active = True

            return self.member_repo.update(existing)

        member = ProviderServiceMember(
            provider_service_offering_id=offering.id,
            provider_membership_id=target_membership.id,
            is_active=True,
        )

        return self.member_repo.create(member)

    def remove_member(
        self,
        *,
        user_id: UUID,
        offering_id: UUID,
        member_id: UUID,
    ):
        manager_membership = self.require_manager(
            user_id=user_id,
        )

        self.get_offering_for_organization(
            offering_id=offering_id,
            organization_id=manager_membership.organization_id,
        )

        member = self.member_repo.get_by_id(
            member_id=member_id,
            offering_id=offering_id,
        )

        if member is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Service member assignment not found.",
            )

        if not member.is_active:
            return member

        member.is_active = False

        return self.member_repo.update(member)
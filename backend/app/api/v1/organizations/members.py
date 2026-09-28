from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.dependencies.provider import (
    get_current_provider_membership,
    require_provider_manager,
)
from app.dependencies.core import DBSession
from app.models.provider_membership import ProviderMembership
from app.schemas.provider_membership import (
    ProviderMemberInvitationCreate,
    ProviderMemberListResponse,
    ProviderMemberResponse,
    ProviderMembershipResponse,
    ProviderMembershipUpdate,
)
from app.services.provider_membership_service import (
    ProviderMembershipService,
)


router = APIRouter(
    prefix="/organizations/me/members",
    tags=["Organization Members"],
)


# Return all members of the authenticated provider organization.
@router.get(
    "",
    response_model=ProviderMemberListResponse,
    status_code=status.HTTP_200_OK,
)
def list_members(
    db: DBSession,
    membership: ProviderMembership = Depends(
        get_current_provider_membership,
    ),
) -> ProviderMemberListResponse:
    service = ProviderMembershipService(db)

    members = service.list_members(
        organization_id=membership.organization_id,
    )

    items = [
        ProviderMemberResponse(
            id=member.id,
            user_id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            role=member.role,
            agent_type=member.agent_type,
            status=member.status,
            invited_at=member.invited_at,
            joined_at=member.joined_at,
        )
        for member, user in members
    ]

    return ProviderMemberListResponse(items=items)


# Invite a manager or agent to the organization.
@router.post(
    "/invitations",
    response_model=ProviderMembershipResponse,
    status_code=status.HTTP_201_CREATED,
)
def invite_member(
    data: ProviderMemberInvitationCreate,
    db: DBSession,
    membership: ProviderMembership = Depends(
        require_provider_manager,
    ),
) -> ProviderMembershipResponse:
    service = ProviderMembershipService(db)

    new_membership = service.invite_member(
        organization_id=membership.organization_id,
        actor=membership,
        data=data,
    )

    db.commit()
    db.refresh(new_membership)

    return new_membership


# Update a manager or agent membership.
@router.patch(
    "/{membership_id}",
    response_model=ProviderMembershipResponse,
    status_code=status.HTTP_200_OK,
)
def update_member(
    membership_id: UUID,
    data: ProviderMembershipUpdate,
    db: DBSession,
    membership: ProviderMembership = Depends(
        require_provider_manager,
    ),
) -> ProviderMembershipResponse:
    service = ProviderMembershipService(db)

    updated_membership = service.update_member(
        organization_id=membership.organization_id,
        membership_id=membership_id,
        actor=membership,
        data=data,
    )

    db.commit()
    db.refresh(updated_membership)

    return updated_membership


# Remove a manager or agent from the organization.
@router.delete(
    "/{membership_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def remove_member(
    membership_id: UUID,
    db: DBSession,
    membership: ProviderMembership = Depends(
        require_provider_manager,
    ),
) -> None:
    service = ProviderMembershipService(db)

    service.remove_member(
        organization_id=membership.organization_id,
        membership_id=membership_id,
        actor=membership,
    )

    db.commit()


# Suspend a manager or agent.
@router.post(
    "/{membership_id}/suspend",
    response_model=ProviderMembershipResponse,
    status_code=status.HTTP_200_OK,
)
def suspend_member(
    membership_id: UUID,
    db: DBSession,
    membership: ProviderMembership = Depends(
        require_provider_manager,
    ),
) -> ProviderMembershipResponse:
    service = ProviderMembershipService(db)

    suspended_membership = service.suspend_member(
        organization_id=membership.organization_id,
        membership_id=membership_id,
        actor=membership,
    )

    db.commit()
    db.refresh(suspended_membership)

    return suspended_membership


# Reactivate a suspended manager or agent.
@router.post(
    "/{membership_id}/reactivate",
    response_model=ProviderMembershipResponse,
    status_code=status.HTTP_200_OK,
)
def reactivate_member(
    membership_id: UUID,
    db: DBSession,
    membership: ProviderMembership = Depends(
        require_provider_manager,
    ),
) -> ProviderMembershipResponse:
    service = ProviderMembershipService(db)

    reactivated_membership = service.reactivate_member(
        organization_id=membership.organization_id,
        membership_id=membership_id,
        actor=membership,
    )

    db.commit()
    db.refresh(reactivated_membership)

    return reactivated_membership
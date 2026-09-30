from uuid import UUID

from fastapi import APIRouter, Depends, Query, status

from app.dependencies.authorization import get_current_user
from app.dependencies.core import DBSession
from app.enums.provider import (
    AgentType,
    ProviderMembershipRole,
)
from app.models.user import User
from app.repositories.provider_membership import (
    ProviderMembershipRepository,
)
from app.repositories.provider_organization import (
    ProviderOrganizationRepository,
)
from app.schemas.provider_membership import (
    AddOrganizationMemberRequest,
    OrganizationMemberResponse,
    UpdateOrganizationMemberRequest,
)
from app.services.provider_membership_service import (
    ProviderMembershipService,
)


router = APIRouter(
    prefix="/organizations",
    tags=["Organization Members"],
)


def get_membership_service(
    db: DBSession,
) -> ProviderMembershipService:

    return ProviderMembershipService(
        db=db,
        membership_repository=ProviderMembershipRepository(db),
        organization_repository=ProviderOrganizationRepository(db),
    )


@router.post(
    "/{organization_id}/members",
    response_model=OrganizationMemberResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_member(
    organization_id: UUID,
    payload: AddOrganizationMemberRequest,
    current_user: User = Depends(get_current_user),
    service: ProviderMembershipService = Depends(
        get_membership_service,
    ),
):

    return service.add_member(
        actor_user_id=current_user.id,
        organization_id=organization_id,
        user_id=payload.user_id,
        role=payload.role,
        agent_type=payload.agent_type,
    )


@router.patch(
    "/{organization_id}/members/{membership_id}",
    response_model=OrganizationMemberResponse,
)
def update_member(
    organization_id: UUID,
    membership_id: UUID,
    payload: UpdateOrganizationMemberRequest,
    current_user: User = Depends(get_current_user),
    service: ProviderMembershipService = Depends(
        get_membership_service,
    ),
):

    return service.update_member(
        actor_user_id=current_user.id,
        organization_id=organization_id,
        membership_id=membership_id,
        role=payload.role,
        agent_type=payload.agent_type,
    )


@router.delete(
    "/{organization_id}/members/{membership_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def remove_member(
    organization_id: UUID,
    membership_id: UUID,
    current_user: User = Depends(get_current_user),
    service: ProviderMembershipService = Depends(
        get_membership_service,
    ),
):

    service.remove_member(
        actor_user_id=current_user.id,
        organization_id=organization_id,
        membership_id=membership_id,
    )

    return None
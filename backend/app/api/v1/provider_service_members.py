from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.dependencies.authorization import get_current_user
from app.dependencies.core import DBSession
from app.models.user import User
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
    ProviderServiceMemberListResponse,
    ProviderServiceMemberResponse,
)
from app.services.provider_service_member import (
    ProviderServiceMemberService,
)


router = APIRouter(
    prefix="/provider/service-offerings",
    tags=["Provider Service Members"],
)


def get_provider_service_member_service(
    db: DBSession,
) -> ProviderServiceMemberService:
    return ProviderServiceMemberService(
        db=db,
        member_repo=ProviderServiceMemberRepository(db),
        offering_repo=ProviderServiceOfferingRepository(db),
        membership_repo=ProviderMembershipRepository(db),
    )


@router.get(
    "/{offering_id}/members",
    response_model=ProviderServiceMemberListResponse,
)
def list_service_members(
    offering_id: UUID,
    current_user: User = Depends(get_current_user),
    service: ProviderServiceMemberService = Depends(
        get_provider_service_member_service,
    ),
):
    return {
        "items": service.list_members(
            user_id=current_user.id,
            offering_id=offering_id,
        ),
    }


@router.post(
    "/{offering_id}/members",
    response_model=ProviderServiceMemberResponse,
    status_code=status.HTTP_201_CREATED,
)
def assign_service_member(
    offering_id: UUID,
    payload: ProviderServiceMemberCreateRequest,
    current_user: User = Depends(get_current_user),
    service: ProviderServiceMemberService = Depends(
        get_provider_service_member_service,
    ),
):
    return service.assign_member(
        user_id=current_user.id,
        offering_id=offering_id,
        payload=payload,
    )


@router.delete(
    "/{offering_id}/members/{member_id}",
    response_model=ProviderServiceMemberResponse,
)
def remove_service_member(
    offering_id: UUID,
    member_id: UUID,
    current_user: User = Depends(get_current_user),
    service: ProviderServiceMemberService = Depends(
        get_provider_service_member_service,
    ),
):
    return service.remove_member(
        user_id=current_user.id,
        offering_id=offering_id,
        member_id=member_id,
    )
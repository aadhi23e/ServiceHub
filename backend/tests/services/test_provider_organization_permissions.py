import pytest

from app.enums.provider import (
    MembershipStatus,
    ProviderMembershipRole,
)
from app.exceptionsauthorization import AuthorizationError
from app.services.provider_organization_service import (
    ProviderOrganizationService,
)


def create_membership(
    role: ProviderMembershipRole,
    status: MembershipStatus = MembershipStatus.ACTIVE,
):
    return type(
        "Membership",
        (),
        {
            "role": role,
            "status": status,
            "organization_id": None,
        },
    )()


def test_owner_can_manage_organization(db_session):
    service = ProviderOrganizationService(db_session)

    owner = create_membership(
        ProviderMembershipRole.OWNER,
    )

    service._require_manager(owner)


def test_manager_can_manage_organization(db_session):
    service = ProviderOrganizationService(db_session)

    manager = create_membership(
        ProviderMembershipRole.MANAGER,
    )

    service._require_manager(manager)


def test_agent_cannot_manage_organization(db_session):
    service = ProviderOrganizationService(db_session)

    agent = create_membership(
        ProviderMembershipRole.AGENT,
    )

    with pytest.raises(AuthorizationError):
        service._require_manager(agent)


def test_suspended_manager_cannot_manage_organization(db_session):
    service = ProviderOrganizationService(db_session)

    manager = create_membership(
        ProviderMembershipRole.MANAGER,
        status=MembershipStatus.SUSPENDED,
    )

    with pytest.raises(AuthorizationError):
        service._require_manager(manager)


def test_suspended_owner_cannot_manage_organization(db_session):
    service = ProviderOrganizationService(db_session)

    owner = create_membership(
        ProviderMembershipRole.OWNER,
        status=MembershipStatus.SUSPENDED,
    )

    with pytest.raises(AuthorizationError):
        service._require_manager(owner)
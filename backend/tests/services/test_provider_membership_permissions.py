import pytest

from app.enums.provider import ProviderMembershipRole
from app.exceptions.authorization import AuthorizationError
from app.services.provider_membership_service import (
    ProviderMembershipService,
)


def create_membership(
    role: ProviderMembershipRole,
):
    return type(
        "Membership",
        (),
        {
            "role": role,
        },
    )()


def test_owner_can_manage_manager(db_session):
    service = ProviderMembershipService(db_session)

    owner = create_membership(
        ProviderMembershipRole.OWNER,
    )

    service._validate_management_permission(
        actor=owner,
        target_role=ProviderMembershipRole.MANAGER,
    )


def test_owner_can_manage_agent(db_session):
    service = ProviderMembershipService(db_session)

    owner = create_membership(
        ProviderMembershipRole.OWNER,
    )

    service._validate_management_permission(
        actor=owner,
        target_role=ProviderMembershipRole.AGENT,
    )


def test_manager_can_manage_agent(db_session):
    service = ProviderMembershipService(db_session)

    manager = create_membership(
        ProviderMembershipRole.MANAGER,
    )

    service._validate_management_permission(
        actor=manager,
        target_role=ProviderMembershipRole.AGENT,
    )


def test_manager_cannot_manage_manager(db_session):
    service = ProviderMembershipService(db_session)

    manager = create_membership(
        ProviderMembershipRole.MANAGER,
    )

    with pytest.raises(AuthorizationError):
        service._validate_management_permission(
            actor=manager,
            target_role=ProviderMembershipRole.MANAGER,
        )


def test_manager_cannot_manage_owner(db_session):
    service = ProviderMembershipService(db_session)

    manager = create_membership(
        ProviderMembershipRole.MANAGER,
    )

    with pytest.raises(AuthorizationError):
        service._validate_management_permission(
            actor=manager,
            target_role=ProviderMembershipRole.OWNER,
        )


def test_agent_cannot_manage_agent(db_session):
    service = ProviderMembershipService(db_session)

    agent = create_membership(
        ProviderMembershipRole.AGENT,
    )

    with pytest.raises(AuthorizationError):
        service._validate_management_permission(
            actor=agent,
            target_role=ProviderMembershipRole.AGENT,
        )


def test_owner_cannot_manage_owner(db_session):
    service = ProviderMembershipService(db_session)

    owner = create_membership(
        ProviderMembershipRole.OWNER,
    )

    with pytest.raises(AuthorizationError):
        service._validate_management_permission(
            actor=owner,
            target_role=ProviderMembershipRole.OWNER,
        )
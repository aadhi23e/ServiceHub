from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.enums.provider import (
    MembershipStatus,
    ProviderMembershipRole,
    ProviderStatus,
)
from app.models.provider_membership import ProviderMembership
from app.models.provider_organization import ProviderOrganization
from app.models.provider_profile import ProviderProfile
from app.models.user import User


class AuthRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    # Find a user by email.
    def get_user_by_email(self, email: str) -> User | None:
        statement = select(User).where(User.email == email)

        return self.db.execute(statement).scalar_one_or_none()

    # Find a user by UUID.
    def get_user_by_id(self, user_id: UUID) -> User | None:
        statement = select(User).where(User.id == user_id)

        return self.db.execute(statement).scalar_one_or_none()

    # Persist a new customer user.
    def create_user(self, user: User) -> User:
        self.db.add(user)
        self.db.flush()

        return user

    # Create the provider profile, organization, and owner membership.
    def create_provider_account(
        self,
        *,
        user: User,
        display_name: str,
        organization_name: str,
        legal_name: str | None,
    ) -> ProviderOrganization:
        self.db.add(user)
        self.db.flush()

        provider_profile = ProviderProfile(
            user_id=user.id,
            display_name=display_name,
            business_contact_email=user.email,
            business_contact_phone=user.phone,
        )

        self.db.add(provider_profile)
        self.db.flush()

        organization = ProviderOrganization(
            name=organization_name,
            legal_name=legal_name,
            status=ProviderStatus.PENDING,
            created_by=user.id,
        )

        self.db.add(organization)
        self.db.flush()

        membership = ProviderMembership(
            user_id=user.id,
            organization_id=organization.id,
            role=ProviderMembershipRole.OWNER,
            agent_type=None,
            status=MembershipStatus.ACTIVE,
        )

        self.db.add(membership)
        self.db.flush()

        return organization

    # Update the timestamp after a successful login.
    def update_last_login(self, user: User) -> User:
        user.last_login_at = datetime.now(UTC)

        self.db.flush()

        return user
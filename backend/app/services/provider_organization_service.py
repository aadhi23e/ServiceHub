from math import ceil
from uuid import UUID

from sqlalchemy.orm import Session

from app.enums.provider import (
    MembershipStatus,
    ProviderMembershipRole,
    ProviderStatus,
)
from app.core.exceptions import AuthorizationError
from app.core.exceptions import ConflictError
from app.core.exceptions import ResourceNotFoundError
from app.models.provider_membership import ProviderMembership
from app.models.provider_organization import ProviderOrganization
from app.repositories.provider_organization_repository import (
    ProviderOrganizationRepository,
)
from app.schemas.provider_organization import (
    ProviderOrganizationUpdate,
    ProviderOrganizationCreate
)
from app.enums.user import UserRole
from app.enums.provider import VerificationStatus
from app.models import (
    ProviderVerification,
    ProviderProfile,
    User
)

class ProviderOrganizationService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = ProviderOrganizationRepository(db)

    # Create the provider profile, organization, owner membership,
    # and verification request for an authenticated customer.
    def create_provider_organization(
        self,
        *,
        user: User,
        data: ProviderOrganizationCreate,
    ) -> ProviderOrganization:
        if user.role != UserRole.CUSTOMER:
            raise ConflictError(
                code="INVALID_PROVIDER_CONVERSION",
                message="Only customer accounts can create a provider organization.",
            )

        existing_membership = (
            self.repository.get_active_membership_by_user(
                user_id=user.id,
            )
        )

        if existing_membership is not None:
            raise ConflictError(
                code="PROVIDER_ORGANIZATION_EXISTS",
                message="This account already belongs to a provider organization.",
            )

        provider_profile = ProviderProfile(
            user_id=user.id,
            display_name=data.display_name.strip(),
            business_contact_email=user.email,
            business_contact_phone=user.phone,
        )

        organization = ProviderOrganization(
            name=data.organization_name.strip(),
            legal_name=(
                data.legal_name.strip()
                if data.legal_name
                else None
            ),
            status=ProviderStatus.PENDING,
            created_by=user.id,
        )

        self.db.add(provider_profile)
        self.db.flush()

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

        verification = ProviderVerification(
            organization_id=organization.id,
            # provider_profile_id=provider_profile.id,
            status=VerificationStatus.PENDING,
        )

        self.db.add(verification)
        self.db.flush()

        user.role = UserRole.PROVIDER
        self.db.flush()

        return organization
    
    # Return public organizations.
    def list_public(
        self,
        search: str | None,
        page: int,
        page_size: int,
    ) -> tuple[list[ProviderOrganization], int, int]:
        offset = (page - 1) * page_size

        organizations, total = self.repository.list_public(
            search=search,
            offset=offset,
            limit=page_size,
        )

        total_pages = ceil(total / page_size) if total else 0

        return organizations, total, total_pages

    # Return one active organization for public access.
    def get_public(
        self,
        organization_id: UUID,
    ) -> ProviderOrganization:
        organization = self.repository.get_public_by_id(
            organization_id=organization_id,
        )

        if organization is None:
            raise ResourceNotFoundError(
                message="Organization not found.",
            )

        return organization

    # Return the organization belonging to the current provider.
    def get_my_organization(
        self,
        membership: ProviderMembership,
    ) -> ProviderOrganization:
        organization = self.repository.get_by_id(
            organization_id=membership.organization_id,
        )

        if organization is None:
            raise ResourceNotFoundError(
                message="Provider organization not found.",
            )

        return organization

    # Update the authenticated provider's organization.
    def update_my_organization(
        self,
        membership: ProviderMembership,
        data: ProviderOrganizationUpdate,
    ) -> ProviderOrganization:
        self._require_manager(membership)

        organization = self.repository.get_by_id(
            organization_id=membership.organization_id,
        )

        if organization is None:
            raise ResourceNotFoundError(
                message="Provider organization not found.",
            )

        if organization.status in {
            ProviderStatus.SUSPENDED,
            ProviderStatus.DEACTIVATED,
        }:
            raise ConflictError(
                message="This organization cannot be updated in its current status.",
            )

        if data.name is not None:
            organization.name = data.name

        if data.legal_name is not None:
            organization.legal_name = data.legal_name

        if data.description is not None:
            organization.description = data.description

        return self.repository.update(organization)

    # Return an organization for administrative use.
    def get_admin_organization(
        self,
        organization_id: UUID,
    ) -> ProviderOrganization:
        organization = self.repository.get_by_id(
            organization_id=organization_id,
        )

        if organization is None:
            raise ResourceNotFoundError(
                message="Organization not found.",
            )

        return organization

    # Return all organizations for administrative use.
    def list_admin(
        self,
        search: str | None,
        status: ProviderStatus | None,
        page: int,
        page_size: int,
    ) -> tuple[list[ProviderOrganization], int, int]:
        offset = (page - 1) * page_size

        organizations, total = self.repository.list_admin(
            search=search,
            status=status,
            offset=offset,
            limit=page_size,
        )

        total_pages = ceil(total / page_size) if total else 0

        return organizations, total, total_pages

    # Return an administrative organization summary.
    def get_admin_summary(
        self,
        organization_id: UUID,
    ) -> dict:
        organization = self.get_admin_organization(
            organization_id=organization_id,
        )

        member_count = self.repository.count_active_members(
            organization_id=organization.id,
        )

        return {
            "id": organization.id,
            "name": organization.name,
            "status": organization.status,
            "member_count": member_count,
        }

    # Deactivate an organization.
    def deactivate(
        self,
        organization_id: UUID,
    ) -> ProviderOrganization:
        organization = self.get_admin_organization(
            organization_id=organization_id,
        )

        if organization.status == ProviderStatus.DEACTIVATED:
            raise ConflictError(
                message="Organization is already deactivated.",
            )

        organization.status = ProviderStatus.DEACTIVATED

        return self.repository.update(organization)

    # Reactivate an organization.
    def reactivate(
        self,
        organization_id: UUID,
    ) -> ProviderOrganization:
        organization = self.get_admin_organization(
            organization_id=organization_id,
        )

        if organization.status != ProviderStatus.DEACTIVATED:
            raise ConflictError(
                message="Only deactivated organizations can be reactivated.",
            )

        organization.status = ProviderStatus.ACTIVE

        return self.repository.update(organization)

    # Require an OWNER or MANAGER membership.
    def _require_manager(
        self,
        membership: ProviderMembership,
    ) -> None:
        if membership.status != MembershipStatus.ACTIVE:
            raise AuthorizationError(
                message="Active organization membership is required.",
            )

        if membership.role not in {
            ProviderMembershipRole.OWNER,
            ProviderMembershipRole.MANAGER,
        }:
            raise AuthorizationError(
                message="Owner or manager access is required.",
            )
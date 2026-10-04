import math
from uuid import UUID

from fastapi import HTTPException, status

from app.enums.provider import ProviderMembershipRole
from app.models.provider_service_offering import ProviderServiceOffering
from app.repositories.provider_membership import (
    ProviderMembershipRepository,
)
from app.repositories.provider_service_offering import (
    ProviderServiceOfferingRepository,
)
from app.repositories.service import ServiceRepository
from app.schemas.provider_service_offering import (
    ProviderServiceOfferingCreateRequest,
    ProviderServiceOfferingUpdateRequest,
)


class ProviderServiceOfferingService:
    def __init__(
        self,
        *,
        db,
        offering_repo: ProviderServiceOfferingRepository,
        membership_repo: ProviderMembershipRepository,
        service_repo: ServiceRepository,
    ):
        self.db = db
        self.offering_repo = offering_repo
        self.membership_repo = membership_repo
        self.service_repo = service_repo

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
                    "can manage service offerings."
                ),
            )

        return membership

    def list_offerings(
        self,
        *,
        user_id: UUID,
        page: int,
        page_size: int,
    ):
        membership = self.get_provider_membership(
            user_id=user_id,
        )

        items, total = self.offering_repo.list(
            organization_id=membership.organization_id,
            page=page,
            page_size=page_size,
        )

        return {
            "items": items,
            "page": page,
            "page_size": page_size,
            "total": total,
            "total_pages": math.ceil(total / page_size)
            if total
            else 0,
        }

    def create_offering(
        self,
        *,
        user_id: UUID,
        payload: ProviderServiceOfferingCreateRequest,
    ):
        membership = self.require_manager(
            user_id=user_id,
        )

        service = self.service_repo.get_by_id(
            payload.service_id,
        )

        if service is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Service not found.",
            )

        if not service.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot offer an inactive service.",
            )

        existing = self.offering_repo.get_by_service(
            organization_id=membership.organization_id,
            service_id=payload.service_id,
        )

        if existing is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=(
                    "Your organization already offers this service."
                ),
            )

        offering = ProviderServiceOffering(
            organization_id=membership.organization_id,
            service_id=payload.service_id,
            price=payload.price,
            currency=payload.currency,
            duration_minutes=payload.duration_minutes,
            buffer_minutes=payload.buffer_minutes,
            service_modes=payload.service_modes,
            is_active=True,
        )

        self.offering_repo.create(offering)
        self.db.commit()
        return offering
    
    def get_offering(
        self,
        *,
        user_id: UUID,
        offering_id: UUID,
    ):
        membership = self.get_provider_membership(
            user_id=user_id,
        )

        offering = self.offering_repo.get_by_id(
            offering_id=offering_id,
            organization_id=membership.organization_id,
        )

        if offering is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Service offering not found.",
            )

        return offering

    def update_offering(
        self,
        *,
        user_id: UUID,
        offering_id: UUID,
        payload: ProviderServiceOfferingUpdateRequest,
    ):
        membership = self.require_manager(
            user_id=user_id,
        )

        offering = self.offering_repo.get_by_id(
            offering_id=offering_id,
            organization_id=membership.organization_id,
        )

        if offering is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Service offering not found.",
            )

        data = payload.model_dump(
            exclude_unset=True,
        )

        if not data:
            return offering

        if "service_id" in data:
            service = self.service_repo.get_by_id(
                data["service_id"],
            )

            if service is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Service not found.",
                )

            if not service.is_active:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Cannot use an inactive service.",
                )

            existing = self.offering_repo.get_by_service(
                organization_id=membership.organization_id,
                service_id=data["service_id"],
            )

            if (
                existing is not None
                and existing.id != offering.id
            ):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=(
                        "Your organization already offers "
                        "this service."
                    ),
                )

        for field, value in data.items():
            setattr(offering, field, value)

        self.db.flush()
        self.db.commit()
        self.db.refresh(offering)

        return offering

    def activate_offering(
        self,
        *,
        user_id: UUID,
        offering_id: UUID,
    ):
        membership = self.require_manager(
            user_id=user_id,
        )

        offering = self.offering_repo.get_by_id(
            offering_id=offering_id,
            organization_id=membership.organization_id,
        )

        if offering is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Service offering not found.",
            )

        if not offering.is_active:
            service = self.service_repo.get_by_id(
                offering.service_id,
            )

            if service is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Service not found.",
                )

            if not service.is_active:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=(
                        "Cannot activate an offering for "
                        "an inactive service."
                    ),
                )

            offering.is_active = True

            self.db.flush()
            self.db.commit()
            self.db.refresh(offering)

        return offering

    def deactivate_offering(
        self,
        *,
        user_id: UUID,
        offering_id: UUID,
    ):
        membership = self.require_manager(
            user_id=user_id,
        )

        offering = self.offering_repo.get_by_id(
            offering_id=offering_id,
            organization_id=membership.organization_id,
        )

        if offering is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Service offering not found.",
            )

        if offering.is_active:
            offering.is_active = False

            self.db.flush()
            self.db.commit()
            self.db.refresh(offering)

        return offering
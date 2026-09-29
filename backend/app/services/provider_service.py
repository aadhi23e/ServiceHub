from sqlalchemy.orm import Session

from app.core.exceptions import ResourceNotFoundError
from app.models.provider_profile import ProviderProfile
from app.repositories.provider_repository import ProviderRepositoryRepository
from app.schemas.provider import ProviderUpdateRequest


class ProviderService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.provider_repository = ProviderRepositoryRepository(db)

    def get_provider(
        self,
        provider: ProviderProfile,
    ) -> ProviderProfile:
        return provider

    def create_provider(
        self,
        # provider: ProviderProfile,
        request: ProviderUpdateRequest,
        user_id: int,
    ) -> ProviderProfile:

        provider = ProviderProfile(
            user_id=user_id,
            business_name=request.business_name,
            description=request.description,
            phone=request.phone,
            address=request.address,
            city=request.city,
            timezone=request.timezone,
        )

        try:
            self.provider_repository.create(provider)
            self.db.commit()
            self.db.refresh(provider)
        except InterruptedError as exc:
            self.db.rollback()

        return provider

    def update_provider(
        self,
        provider: ProviderProfile,
        request: ProviderUpdateRequest,
    ) -> ProviderProfile:
        updated_provider = self.provider_repository.update(
            provider,
            business_name=request.business_name,
            description=request.description,
            phone=request.phone,
            address=request.address,
            city=request.city,
            timezone=request.timezone,
        )

        self.db.commit()
        self.db.refresh(updated_provider)

        return updated_provider

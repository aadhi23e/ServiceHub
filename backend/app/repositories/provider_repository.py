from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.provider import ProviderProfile


class ProviderRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(
        self,
        provider_id: int,
    ) -> ProviderProfile | None:
        statement = select(ProviderProfile).where(ProviderProfile.id == provider_id)

        return self.db.scalar(statement)

    def get_by_user_id(
        self,
        user_id: int,
    ) -> ProviderProfile | None:
        statement = select(ProviderProfile).where(ProviderProfile.user_id == user_id)

        return self.db.scalar(statement)

    def create(
        self,
        provider: ProviderProfile,
    ) -> ProviderProfile:
        self.db.add(provider)

        self.db.flush()

        return provider

    def update(
        self,
        provider: ProviderProfile,
        *,
        business_name: str | None = None,
        description: str | None = None,
        phone: str | None = None,
        address: str | None = None,
        city: str | None = None,
        timezone: str | None = None,
    ) -> ProviderProfile:
        if business_name is not None:
            provider.business_name = business_name

        if description is not None:
            provider.description = description

        if phone is not None:
            provider.phone = phone

        if address is not None:
            provider.address = address

        if city is not None:
            provider.city = city

        if timezone is not None:
            provider.timezone = timezone

        self.db.flush()

        return provider

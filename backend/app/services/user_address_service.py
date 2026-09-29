# backend/app/services/user_address_service.py

from uuid import UUID, uuid4

from sqlalchemy.orm import Session

from app.core.exceptions import ConflictError
from app.core.exceptions import ResourceNotFoundError
from app.models.address import Address
from app.models.user_address import UserAddress
from app.repositories.address_repository import AddressRepository
from app.repositories.user_address_repository import UserAddressRepository


class UserAddressService:
    """
    Handles customer saved-address operations.
    """

    def __init__(self, db: Session):
        self.db = db
        self.address_repository = AddressRepository(db)
        self.user_address_repository = UserAddressRepository(db)

    def list_addresses(
        self,
        *,
        user_id: UUID,
    ) -> list[UserAddress]:
        """
        Return all addresses belonging to the authenticated user.
        """

        return self.user_address_repository.list_for_user(
            user_id=user_id,
        )

    def create_address(
        self,
        *,
        user_id: UUID,
        address_line_1: str,
        address_line_2: str | None,
        landmark: str | None,
        city: str,
        state: str,
        postal_code: str,
        country_code: str,
        latitude: float | None,
        longitude: float | None,
        label: str | None,
        is_default: bool,
    ) -> UserAddress:
        """
        Create a physical address and associate it with the authenticated user.
        """

        existing_addresses = self.user_address_repository.list_for_user(
            user_id=user_id,
        )

        # The first saved address automatically becomes the default.
        if not existing_addresses:
            is_default = True

        if is_default:
            self.user_address_repository.clear_default_for_user(
                user_id
            )

        address = Address(
            id=uuid4(),
            address_line_1=address_line_1.strip(),
            address_line_2=address_line_2,
            landmark=landmark,
            city=city.strip(),
            state=state.strip(),
            postal_code=postal_code.strip(),
            country_code=country_code.upper(),
            latitude=latitude,
            longitude=longitude,
        )

        self.address_repository.create(address)

        user_address = UserAddress(
            id=uuid4(),
            user_id=user_id,
            address_id=address.id,
            label=label,
            is_default=is_default,
        )

        self.user_address_repository.create(user_address)

        return user_address

    def update_address(
        self,
        *,
        user_id: UUID,
        user_address_id: UUID,
        address_line_1: str | None,
        address_line_2: str | None,
        landmark: str | None,
        city: str | None,
        state: str | None,
        postal_code: str | None,
        country_code: str | None,
        latitude: float | None,
        longitude: float | None,
        label: str | None,
    ) -> UserAddress:
        """
        Update an address owned by the authenticated user.
        """

        user_address = self.user_address_repository.get_for_user(
            user_id=user_id,
            user_address_id=user_address_id,
        )

        if user_address is None:
            raise ResourceNotFoundError(
                message="Address not found."
            )

        address = self.address_repository.get_by_id(
            user_address.address_id
        )

        if address is None:
            raise ResourceNotFoundError(
                message="Address record not found."
            )

        if address_line_1 is not None:
            address.address_line_1 = address_line_1.strip()

        if address_line_2 is not None:
            address.address_line_2 = address_line_2

        if landmark is not None:
            address.landmark = landmark

        if city is not None:
            address.city = city.strip()

        if state is not None:
            address.state = state.strip()

        if postal_code is not None:
            address.postal_code = postal_code.strip()

        if country_code is not None:
            address.country_code = country_code.upper()

        if latitude is not None:
            address.latitude = latitude

        if longitude is not None:
            address.longitude = longitude

        if label is not None:
            user_address.label = label

        self.db.flush()

        return user_address

    def set_default(
        self,
        *,
        user_id: UUID,
        user_address_id: UUID,
    ) -> UserAddress:
        """
        Set one saved address as the customer's default address.
        """

        user_address = self.user_address_repository.get_for_user(
            user_id=user_id,
            user_address_id=user_address_id,
        )

        if user_address is None:
            raise ResourceNotFoundError(
                message="Address not found."
            )

        self.user_address_repository.clear_default_for_user(
            user_id
        )

        user_address.is_default = True

        self.db.flush()

        return user_address

    def delete_address(
        self,
        *,
        user_id: UUID,
        user_address_id: UUID,
    ) -> None:
        """
        Remove a saved address belonging to the authenticated user.
        """

        user_address = self.user_address_repository.get_for_user(
            user_id=user_id,
            user_address_id=user_address_id,
        )

        if user_address is None:
            raise ResourceNotFoundError(
                message="Address not found."
            )

        self.user_address_repository.delete(user_address)

        address = self.address_repository.get_by_id(
            user_address.address_id
        )

        if address is not None:
            self.address_repository.delete(address)
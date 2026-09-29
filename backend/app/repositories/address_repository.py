# backend/app/repositories/address_repository.py

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.address import Address


class AddressRepository:
    """
    Handles database operations for addresses owned by users.
    """

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(
        self,
        address_id: UUID,
    ) -> Address | None:
        """
        Return an address by ID.
        """

        statement = select(Address).where(
            Address.id == address_id,
        )

        return self.db.scalar(statement)

    def get_for_user(
        self,
        *,
        address_id: UUID,
        user_id: UUID,
    ) -> Address | None:
        """
        Return an address only when it belongs to the specified user.

        This ownership condition prevents one customer from accessing
        another customer's address by changing the address ID.
        """

        statement = select(Address).where(
            Address.id == address_id,
            Address.user_id == user_id,
        )

        return self.db.scalar(statement)

    def list_for_user(
        self,
        *,
        user_id: UUID,
    ) -> list[Address]:
        """
        Return all addresses belonging to a user.
        """

        statement = (
            select(Address)
            .where(
                Address.user_id == user_id,
            )
            .order_by(
                Address.is_default.desc(),
                Address.created_at.desc(),
            )
        )

        return list(
            self.db.scalars(statement).all()
        )

    def create(
        self,
        address: Address,
    ) -> Address:
        """
        Add a new address and flush the transaction.
        """

        self.db.add(address)
        self.db.flush()

        return address

    def update(
        self,
        address: Address,
    ) -> Address:
        """
        Flush changes made to an address.
        """

        self.db.flush()

        return address

    def delete(
        self,
        address: Address,
    ) -> None:
        """
        Delete an address.
        """

        self.db.delete(address)
        self.db.flush()

    def clear_default_for_user(
        self,
        *,
        user_id: UUID,
    ) -> None:
        """
        Remove the default flag from all addresses owned by a user.
        """

        statement = (
            select(Address)
            .where(
                Address.user_id == user_id,
                Address.is_default.is_(True),
            )
        )

        addresses = self.db.scalars(statement).all()

        for address in addresses:
            address.is_default = False

        self.db.flush()
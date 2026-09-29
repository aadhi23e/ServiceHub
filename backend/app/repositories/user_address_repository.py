# backend/app/repositories/user_address_repository.py

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user_address import UserAddress


class UserAddressRepository:
    """
    Handles the relationship between users and their saved addresses.
    """

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(
        self,
        *,
        user_address_id: UUID,
    ) -> UserAddress | None:
        """
        Return a saved-address relationship by ID.
        """

        statement = select(UserAddress).where(
            UserAddress.id == user_address_id
        )

        return self.db.scalar(statement)

    def get_for_user(
        self,
        *,
        user_id: UUID,
        user_address_id: UUID,
    ) -> UserAddress | None:
        """
        Return a saved address only when it belongs to the specified user.

        This ownership check is important for preventing IDOR.
        """

        statement = select(UserAddress).where(
            UserAddress.id == user_address_id,
            UserAddress.user_id == user_id,
        )

        return self.db.scalar(statement)

    def list_for_user(
        self,
        *,
        user_id: UUID,
    ) -> list[UserAddress]:
        """
        Return all saved addresses belonging to a user.
        """

        statement = (
            select(UserAddress)
            .where(UserAddress.user_id == user_id)
            .order_by(
                UserAddress.is_default.desc(),
                UserAddress.created_at.desc(),
            )
        )

        return list(self.db.scalars(statement).all())

    def create(self, user_address: UserAddress) -> UserAddress:
        """
        Add a user-address relationship.
        """

        self.db.add(user_address)
        self.db.flush()

        return user_address

    def delete(self, user_address: UserAddress) -> None:
        """
        Delete a user-address relationship.
        """

        self.db.delete(user_address)
        self.db.flush()

    def clear_default_for_user(self, user_id: UUID) -> None:
        """
        Remove the default flag from all saved addresses belonging to a user.
        """

        statement = (
            select(UserAddress)
            .where(UserAddress.user_id == user_id)
        )

        relationships = self.db.scalars(statement).all()

        for relationship in relationships:
            relationship.is_default = False

        self.db.flush()
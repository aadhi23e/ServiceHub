# backend/app/services/user_service.py

from uuid import UUID

from sqlalchemy.orm import Session

from app.core.exceptions import ResourceNotFoundError
from app.models.user import User
from app.repositories.user_repository import UserRepository


class UserService:
    """
    Handles authenticated-user account operations.
    """

    def __init__(self, db: Session):
        self.db = db
        self.user_repository = UserRepository(db)

    def get_current_user(self, user_id: UUID) -> User:
        """
        Return the authenticated user's account.
        """

        user = self.user_repository.get_by_id(user_id)

        if user is None:
            raise ResourceNotFoundError(
                message="User not found."
            )

        return user

    def update_current_user(
        self,
        *,
        user_id: UUID,
        first_name: str | None,
        last_name: str | None,
        phone: str | None,
    ) -> User:
        """
        Update fields that the authenticated user is allowed to change.
        """

        user = self.get_current_user(user_id)

        if first_name is not None:
            user.first_name = first_name.strip()

        if last_name is not None:
            user.last_name = last_name.strip()

        if phone is not None:
            user.phone = phone.strip()

        self.user_repository.update(user)

        return user
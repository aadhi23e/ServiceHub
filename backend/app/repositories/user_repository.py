# backend/app/repositories/user_repository.py

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User
from app.enums.user import UserStatus

class UserRepository:
    """
    Handles database operations for User records.
    """

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: UUID) -> User | None:
        """
        Return a user by primary key.
        """

        statement = select(User).where(User.id == user_id)

        return self.db.scalar(statement)

    def update(self, user: User) -> User:
        """
        Flush an updated user without committing the transaction.
        """

        self.db.flush()

        return user
    
    def list_users(
        self,
        *,
        offset: int = 0,
        limit: int = 50,
    ) -> list[User]:
        return self.db.query(User).order_by(User.id).offset(offset).limit(limit).all()

    def suspend(self, user: User) -> User:
        user.status = UserStatus.SUSPENDED.value

        self.db.flush()

        return user

    def activate(self, user: User) -> User:
        user.status = UserStatus.ACTIVE.value

        self.db.flush()

        return user

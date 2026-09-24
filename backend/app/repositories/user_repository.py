from sqlalchemy import select
from sqlalchemy.orm import Session

from app.enums.user import UserRole, UserStatus
from app.models.user import User


class UserRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, user_id: int) -> User | None:
        statement = select(User).where(User.id == user_id)

        return self.db.scalar(statement)

    def get_by_email(self, email: str) -> User | None:
        statement = select(User).where(User.email == email)

        return self.db.scalar(statement)

    def create(self, user: User) -> User:
        self.db.add(user)
        self.db.flush()

        return user

    def update(
        self,
        user: User,
        *,
        first_name: str | None = None,
        last_name: str | None = None,
        phone: str | None = None,
    ) -> User:
        if first_name is not None:
            user.first_name = first_name

        if last_name is not None:
            user.last_name = last_name

        if phone is not None:
            user.phone = phone

        self.db.flush()

        return user

    def update_admin_fields(
        self,
        user: User,
        *,
        first_name: str | None = None,
        last_name: str | None = None,
        phone: str | None = None,
        role: UserRole | None = None,
        status: UserStatus | None = None,
    ) -> User:
        if first_name is not None:
            user.first_name = first_name

        if last_name is not None:
            user.last_name = last_name

        if phone is not None:
            user.phone = phone

        if role is not None:
            user.role = role.value

        if status is not None:
            user.status = status.value

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

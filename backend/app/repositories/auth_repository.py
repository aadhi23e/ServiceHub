# app/repositories/auth_repository.py

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User


class AuthRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_user_by_email(self, email: str) -> User | None:
        stmt = select(User).where(User.email == email)

        return self.db.execute(stmt).scalar_one_or_none()

    def get_user_by_id(self, user_id):
        stmt = select(User).where(User.id == user_id)

        return self.db.execute(stmt).scalar_one_or_none()

    def create_user(self, user: User) -> User:
        self.db.add(user)
        self.db.flush()

        return user

    def update_last_login(self, user: User) -> User:
        user.last_login_at = datetime.utcnow()

        self.db.flush()

        return user
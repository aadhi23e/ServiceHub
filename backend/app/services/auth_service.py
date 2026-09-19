from redis import Redis
from sqlalchemy.orm import Session

from app.repositories.auth_session_repository import AuthSessionRepository
from app.repositories.user_repository import UserRepository


class AuthService:
    def __init__(
        self,
        db: Session,
        redis_client: Redis,
    ) -> None:
        self.db = db
        self.user_repository = UserRepository(db)
        self.auth_session_repository = AuthSessionRepository(redis_client)

    # TODO:
    # register()
    # login()
    # logout()
    # refresh()
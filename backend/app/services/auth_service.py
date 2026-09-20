from redis import Redis
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.exceptions import ConflictError
from app.core.security import hash_password
from app.enums.user import UserRole, UserStatus
from app.repositories.auth_session_repository import AuthSessionRepository
from app.repositories.user_repository import UserRepository
from app.schemas.auth import RegisterRequest, UserResponse
from app.models.user import User


class AuthService:
    def __init__(self, db: Session, redis_client: Redis) -> None:
        self.db = db
        self.user_repository = UserRepository(db)
        self.auth_session_repository = AuthSessionRepository(redis_client)

    def register(self, request: RegisterRequest) -> UserResponse:
        email = str(request.email).lower()

        existing_user = self.user_repository.get_by_email(email)

        if existing_user is not None:
            raise ConflictError(
                code="EMAIL_ALREADY_EXISTS",
                message="An account with this email already exists.",
            )

        user = User(
            email=email,
            password_hash=hash_password(request.password),
            first_name=request.first_name.strip(),
            last_name=request.last_name.strip(),
            phone=request.phone.strip() if request.phone else None,
            role=UserRole.CUSTOMER.value,
            status=UserStatus.ACTIVE.value,
        )

        try:
            self.user_repository.create(user)
            self.db.commit()
            self.db.refresh(user)
        except IntegrityError as exc:
            self.db.rollback()

            raise ConflictError(
                code="EMAIL_ALREADY_EXISTS",
                message="An account with this email already exists.",
            ) from exc

        return UserResponse.model_validate(user)
    # TODO:
    # register()
    # login()
    # logout()
    # refresh()
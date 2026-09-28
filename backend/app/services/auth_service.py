from redis import Redis
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.exceptions import AuthenticationError, ConflictError
from app.core.security import (
    create_access_token,
    generate_refresh_token,
    hash_password,
    hash_refresh_token,
    verify_password,
)
from app.enums.user import UserRole, UserStatus
from app.models.user import User
from app.repositories.auth_repository import AuthRepository
from app.repositories.auth_session_repository import AuthSessionRepository
from app.schemas.auth import (
    LoginRequest,
    LoginResponse,
    RegisterRequest,
    TokenResponse,
    UserResponse,
)


class AuthService:
    def __init__(
        self,
        db: Session,
        redis_client: Redis,
    ) -> None:
        self.db = db
        self.auth_repository = AuthRepository(db)
        self.auth_session_repository = AuthSessionRepository(
            redis_client,
        )

    # Register a customer or provider account.
    def register(
        self,
        request: RegisterRequest,
    ) -> UserResponse:
        email = str(request.email).lower()

        existing_user = self.auth_repository.get_user_by_email(
            email,
        )

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
            role=request.role,
            status=UserStatus.ACTIVE,
        )

        try:
            if request.role == UserRole.CUSTOMER:
                self.auth_repository.create_user(user)

            elif request.role == UserRole.PROVIDER:
                self.auth_repository.create_provider_account(
                    user=user,
                    display_name=(
                        f"{request.first_name.strip()} "
                        f"{request.last_name.strip()}"
                    ),
                    organization_name=request.organization_name,
                    legal_name=request.legal_name,
                )

            else:
                raise ConflictError(
                    code="INVALID_REGISTRATION_ROLE",
                    message="This user role cannot be registered publicly.",
                )

            self.db.commit()
            self.db.refresh(user)

        except IntegrityError as exc:
            self.db.rollback()

            raise ConflictError(
                code="REGISTRATION_CONFLICT",
                message="The account could not be created because the requested information already exists.",
            ) from exc

        except Exception:
            self.db.rollback()
            raise

        return UserResponse.model_validate(user)

    # Authenticate a customer or provider and create a refresh session.
    def login(
        self,
        request: LoginRequest,
    ) -> tuple[LoginResponse, str]:
        email = str(request.email).lower()

        user = self.auth_repository.get_user_by_email(
            email,
        )

        if user is None:
            raise AuthenticationError(
                message="Invalid email or password.",
            )

        if not verify_password(
            request.password,
            user.password_hash,
        ):
            raise AuthenticationError(
                message="Invalid email or password.",
            )

        if user.status != UserStatus.ACTIVE:
            raise AuthenticationError(
                message="Invalid email or password.",
            )

        if user.role == UserRole.ADMIN:
            raise AuthenticationError(
                message="Invalid email or password.",
            )

        access_token, expires_in = create_access_token(
            user_id=user.id,
            role=user.role.value,
        )

        refresh_token = generate_refresh_token()
        refresh_token_hash = hash_refresh_token(
            refresh_token,
        )

        settings = get_settings()

        refresh_expires_in = (
            settings.refresh_token_expire_days
            * 24
            * 60
            * 60
        )

        self.auth_session_repository.create(
            token_hash=refresh_token_hash,
            user_id=user.id,
            expires_in_seconds=refresh_expires_in,
        )

        try:
            self.auth_repository.update_last_login(user)

            self.db.commit()
            self.db.refresh(user)

        except Exception:
            self.db.rollback()

            self.auth_session_repository.revoke(
                refresh_token_hash,
            )

            raise

        response = LoginResponse(
            user=UserResponse.model_validate(user),
            access_token=access_token,
            token_type="bearer",
            expires_in=expires_in,
        )

        return response, refresh_token

    # Revoke the current refresh session.
    def logout(
        self,
        refresh_token: str | None,
    ) -> None:
        if not refresh_token:
            return

        refresh_token_hash = hash_refresh_token(
            refresh_token,
        )

        self.auth_session_repository.revoke(
            refresh_token_hash,
        )

    # Rotate the refresh token and issue a new access token.
    def refresh(
        self,
        refresh_token: str,
    ) -> tuple[TokenResponse, str]:
        refresh_token_hash = hash_refresh_token(
            refresh_token,
        )

        user_id = self.auth_session_repository.consume(
            refresh_token_hash,
        )

        if user_id is None:
            raise AuthenticationError(
                message="Invalid or expired refresh token.",
            )

        user = self.auth_repository.get_user_by_id(
            user_id,
        )

        if user is None:
            raise AuthenticationError(
                message="Invalid or expired refresh token.",
            )

        if user.status != UserStatus.ACTIVE:
            raise AuthenticationError(
                message="Invalid or expired refresh token.",
            )

        if user.role == UserRole.ADMIN:
            raise AuthenticationError(
                message="Invalid or expired refresh token.",
            )

        access_token, expires_in = create_access_token(
            user_id=user.id,
            role=user.role.value,
        )

        new_refresh_token = generate_refresh_token()

        new_refresh_token_hash = hash_refresh_token(
            new_refresh_token,
        )

        settings = get_settings()

        refresh_expires_in = (
            settings.refresh_token_expire_days
            * 24
            * 60
            * 60
        )

        self.auth_session_repository.create(
            token_hash=new_refresh_token_hash,
            user_id=user.id,
            expires_in_seconds=refresh_expires_in,
        )

        response = TokenResponse(
            access_token=access_token,
            token_type="bearer",
            expires_in=expires_in,
        )

        return response, new_refresh_token
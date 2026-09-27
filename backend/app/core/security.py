import hashlib
import secrets
from datetime import datetime, timedelta, timezone
from uuid import UUID

import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from app.core.config import get_settings
# from app.exceptions.authentication import AuthenticationError
from app.core.exceptions import AuthenticationError


settings = get_settings()
password_hasher = PasswordHasher()


# Hash a user's password with Argon2.
def hash_password(password: str) -> str:
    return password_hasher.hash(password)


# Verify a plain password against its Argon2 hash.
def verify_password(password: str, password_hash: str) -> bool:
    try:
        password_hasher.verify(password_hash, password)
        return True
    except VerifyMismatchError:
        return False


# Generate a secure opaque refresh token.
def generate_refresh_token() -> str:
    return secrets.token_urlsafe(32)


# Hash a refresh token before storing it in Redis.
def hash_refresh_token(refresh_token: str) -> str:
    return hashlib.sha256(refresh_token.encode("utf-8")).hexdigest()


# Create a short-lived JWT access token for a user.
def create_access_token(
    *,
    user_id: UUID,
    role: str,
) -> str:
    now = datetime.now(timezone.utc)
    expires_at = now + timedelta(
        minutes=settings.access_token_expire_minutes
    )

    payload = {
        "sub": str(user_id),
        "role": role,
        "type": "access",
        "iat": now,
        "exp": expires_at,
        "jti": secrets.token_urlsafe(16),
    }

    return jwt.encode(
        payload,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )


# Decode and validate a JWT access token.
def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm],
        )
    except jwt.PyJWTError as exc:
        raise AuthenticationError(
            message="Invalid or expired access token."
        ) from exc

    if payload.get("type") != "access":
        raise AuthenticationError(
            message="Invalid access token."
        )

    if not payload.get("sub"):
        raise AuthenticationError(
            message="Invalid access token."
        )

    return payload
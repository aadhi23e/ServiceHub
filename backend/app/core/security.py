import hashlib
import secrets
from datetime import UTC, datetime, timedelta
from typing import Any

import jwt
from argon2 import PasswordHasher
from argon2.exceptions import (
    InvalidHashError,
    VerificationError,
    VerifyMismatchError,
)

from app.core.config import get_settings
from app.core.exceptions import AuthenticationError

password_hasher = PasswordHasher()

REFRESH_TOKEN_BYTES = 32


def hash_password(password: str) -> str:
    """Hash a password using Argon2id."""
    return password_hasher.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    """Verify a password against an Argon2 hash."""
    try:
        return password_hasher.verify(password_hash, password)
    except (
        VerifyMismatchError,
        VerificationError,
        InvalidHashError,
    ):
        return False


def generate_refresh_token() -> str:
    """Generate a cryptographically secure opaque refresh token."""
    return secrets.token_urlsafe(REFRESH_TOKEN_BYTES)


def hash_refresh_token(refresh_token: str) -> str:
    """Hash a refresh token before storing it."""
    return hashlib.sha256(
        refresh_token.encode("utf-8"),
    ).hexdigest()


def create_access_token(
    *,
    user_id: int,
    role: str,
) -> tuple[str, int]:
    """Create a short-lived JWT access token."""
    settings = get_settings()

    now = datetime.now(UTC)
    expires_delta = timedelta(
        minutes=settings.access_token_expire_minutes,
    )
    expires_at = now + expires_delta

    payload: dict[str, Any] = {
        "sub": str(user_id),
        "role": role,
        "type": "access",
        "iat": now,
        "exp": expires_at,
        "jti": secrets.token_hex(16),
    }

    token = jwt.encode(
        payload,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )

    return token, int(expires_delta.total_seconds())


def decode_access_token(token: str) -> dict[str, Any]:
    """Validate and decode a JWT access token."""
    settings = get_settings()

    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm],
        )
    except jwt.PyJWTError as exc:
        raise AuthenticationError(
            message="Invalid or expired access token.",
        ) from exc

    if payload.get("type") != "access":
        raise AuthenticationError(
            message="Invalid access token.",
        )

    if not payload.get("sub"):
        raise AuthenticationError(
            message="Invalid access token.",
        )

    return payload

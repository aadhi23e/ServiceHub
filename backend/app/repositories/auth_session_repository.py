from uuid import UUID

from redis import Redis


class AuthSessionRepository:
    PREFIX = "auth:session:"

    def __init__(self, redis_client: Redis):
        self.redis = redis_client

    # Build the Redis key for a hashed refresh token.
    def _key(self, token_hash: str) -> str:
        return f"{self.PREFIX}{token_hash}"

    # Store a refresh-token session in Redis.
    def create(
        self,
        *,
        token_hash: str,
        user_id: UUID,
        expires_in_seconds: int,
    ) -> None:
        self.redis.set(
            self._key(token_hash),
            str(user_id),
            ex=expires_in_seconds,
        )

    # Return the user ID associated with a refresh token.
    def get_user_id(self, token_hash: str) -> UUID | None:
        value = self.redis.get(self._key(token_hash))

        if value is None:
            return None

        if isinstance(value, bytes):
            value = value.decode("utf-8")

        try:
            return UUID(str(value))
        except (ValueError, TypeError):
            return None

    # Revoke a refresh-token session.
    def revoke(self, token_hash: str) -> None:
        self.redis.delete(self._key(token_hash))

    # Atomically consume a refresh-token session.
    def consume(self, token_hash: str) -> UUID | None:
        value = self.redis.getdel(self._key(token_hash))

        if value is None:
            return None

        if isinstance(value, bytes):
            value = value.decode("utf-8")

        try:
            return UUID(str(value))
        except (ValueError, TypeError):
            return None
from redis import Redis


class AuthSessionRepository:
    PREFIX = "auth:session:"

    def __init__(self, redis_client: Redis) -> None:
        self.redis = redis_client

    def _key(self, token_hash: str) -> str:
        return f"{self.PREFIX}{token_hash}"

    def create(
        self,
        *,
        token_hash: str,
        user_id: int,
        expires_in_seconds: int,
    ) -> None:
        key = self._key(token_hash)

        self.redis.set(
            key,
            str(user_id),
            ex=expires_in_seconds,
        )

    def get_user_id(self, token_hash: str) -> int | None:
        value = self.redis.get(self._key(token_hash))

        if value is None:
            return None

        return int(value)

    def revoke(self, token_hash: str) -> None:
        self.redis.delete(self._key(token_hash))
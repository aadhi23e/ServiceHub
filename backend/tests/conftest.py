import pytest
from fastapi.testclient import TestClient

from app.core.redis import get_redis
from app.main import app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def redis_client():
    redis = get_redis()

    try:
        yield redis
    finally:
        redis.flushdb()

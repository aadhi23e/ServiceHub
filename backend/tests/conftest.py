import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.redis import get_redis
from app.db.base import Base
from app.main import app
from app.models import *  # noqa: F403

# docker compose exec postgres psql -U servicehub -d servicehub -c "CREATE DATABASE servicehub_test OWNER servicehub;"
TEST_DATABASE_URL = "postgresql+psycopg://servicehub:servicehub@localhost:5432/servicehub_test"


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


@pytest.fixture
def db():
    engine = create_engine(
        TEST_DATABASE_URL,
        pool_pre_ping=True,
    )

    Base.metadata.create_all(engine)

    session_factory = sessionmaker(
        bind=engine,
        autoflush=False,
        expire_on_commit=False,
    )

    session = session_factory()

    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(engine)
        engine.dispose()
import pytest
import pytest_asyncio
import redis.asyncio as redis
from fastapi.testclient import TestClient

from app.main import app

pytest_plugins = ["pytest_asyncio"]


@pytest.fixture
def client():
    """
    A test client for the app
    """
    with TestClient(app) as client:
        yield client


@pytest_asyncio.fixture(autouse=True)
async def flush_redis():
    """
    Flush Redis database before each test.
    """
    redis_connection = redis.from_url("redis://redis", encoding="utf-8", decode_responses=True)
    await redis_connection.flushdb()

    yield

    await redis_connection.aclose()

import pytest

from tests.conftest import client


@pytest.mark.asyncio
async def test_readiness(client):
    """
    Test /monitoring/readiness endpoint
    """

    response = client.get("/monitoring/readiness")

    assert response.status_code == 200

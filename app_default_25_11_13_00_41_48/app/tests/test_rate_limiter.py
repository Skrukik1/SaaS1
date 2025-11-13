import pytest
from httpx import AsyncClient
import asyncio


@pytest.mark.asyncio
async def test_rate_limit_enforcement(client: AsyncClient):
    for _ in range(0, 100):
        response = await client.get("/health")
        assert response.status_code == 200
    # 101st request should be rate limited
    response = await client.get("/health")
    assert response.status_code == 429

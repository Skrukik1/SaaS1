import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_i18n_header(client: AsyncClient):
    response = await client.get("/health", headers={"Accept-Language": "pl"})
    assert response.status_code == 200
    assert response.headers.get("Content-Language") == "pl"


@pytest.mark.asyncio
async def test_i18n_query_param(client: AsyncClient):
    response = await client.get("/health?lang=en")
    assert response.status_code == 200
    assert response.headers.get("Content-Language") == "en"

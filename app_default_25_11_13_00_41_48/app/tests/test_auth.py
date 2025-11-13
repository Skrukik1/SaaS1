import pytest
from httpx import AsyncClient
from app.main import app
from app.schemas.auth import LoginRequest


@pytest.mark.asyncio
async def test_login_success(client: AsyncClient):
    # Setup user fixture or pre-populate DB accordingly
    response = await client.post("/auth/login", data={"username": "testuser", "password": "password123"})
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_failure_wrong_credentials(client: AsyncClient):
    response = await client.post("/auth/login", data={"username": "wrong", "password": "wrong"})
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_protected_endpoint_requires_auth(client: AsyncClient):
    response = await client.get("/users")
    assert response.status_code == 401

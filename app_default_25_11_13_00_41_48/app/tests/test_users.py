import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_user(client: AsyncClient, admin_token: str):
    response = await client.post(
        "/users",
        json={"username": "newuser", "email": "newuser@example.com", "password": "password123", "roles": ["user"]},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "newuser"


@pytest.mark.asyncio
async def test_get_user(client: AsyncClient, admin_token: str):
    response = await client.get("/users/1", headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 200
    data = response.json()
    assert "username" in data


@pytest.mark.asyncio
async def test_update_user(client: AsyncClient, admin_token: str):
    response = await client.put(
        "/users/1",
        json={"email": "updated@example.com"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "updated@example.com"


@pytest.mark.asyncio
async def test_delete_user(client: AsyncClient, admin_token: str):
    response = await client.delete("/users/1", headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 204

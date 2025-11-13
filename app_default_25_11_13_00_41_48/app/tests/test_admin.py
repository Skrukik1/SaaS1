import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_list_roles(client: AsyncClient, admin_token: str):
    response = await client.get("/admin/roles", headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_create_role(client: AsyncClient, admin_token: str):
    response = await client.post(
        "/admin/roles",
        json={"name": "testrole", "description": "Test role", "permissions": {}},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_unauthorized_access(client: AsyncClient):
    response = await client.get("/admin/roles")
    assert response.status_code == 401

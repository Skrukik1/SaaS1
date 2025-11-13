import pytest
from unittest.mock import AsyncMock

@pytest.mark.asyncio
async def test_help_command(bot_client):
    message = AsyncMock()
    message.content = "!help"
    ctx = await bot_client.get_context(message)
    response = await bot_client.invoke(ctx)
    assert response is None  # Assuming help prints to channel, no exception raised

@pytest.mark.asyncio
async def test_admin_command_permission(bot_client):
    message = AsyncMock()
    message.content = "!ban @user"
    message.author.roles = ["user"]
    ctx = await bot_client.get_context(message)
    with pytest.raises(PermissionError):
        await bot_client.invoke(ctx)

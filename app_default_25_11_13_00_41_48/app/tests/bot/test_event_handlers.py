import pytest
from unittest.mock import AsyncMock

@pytest.mark.asyncio
async def test_on_message_spam_detection(bot_client):
    message = AsyncMock()
    message.content = "spam spam spam"
    message.author.id = 123
    # Simulate multiple messages to trigger spam detection
    for _ in range(6):
        await bot_client.on_message(message)
    # Expected: deletion or warning - check mock calls accordingly

@pytest.mark.asyncio
async def test_on_member_join_role_assignment(bot_client):
    member = AsyncMock()
    member.id = 123
    member.guild = AsyncMock()
    await bot_client.on_member_join(member)
    # Check calls to assign default role

import discord
from discord.ext import commands, tasks
import asyncio
import logging
from app.config import settings
from bot.utils.logging import configure_bot_logging
from bot.utils.security import check_permissions, is_spam_message
from bot.utils.i18n import get_translation
from bot.commands.admin import admin_commands
from bot.commands.general import general_commands
from bot.events.on_message import on_message_handler
from bot.events.on_member_join import on_member_join_handler

intents = discord.Intents.default()
intents.members = True
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix=settings.DISCORD_COMMAND_PREFIX, intents=intents)

configure_bot_logging()

# Register commands
for cmd in admin_commands:
    bot.add_command(cmd)

for cmd in general_commands:
    bot.add_command(cmd)


@bot.event
async def on_ready():
    logging.info(f"Discord Bot connected as {bot.user} (ID: {bot.user.id})")


@bot.event
async def on_message(message):
    if message.author == bot.user or message.author.bot:
        return
    if await is_spam_message(message):
        await message.delete()
        await message.channel.send(f"{message.author.mention} Please stop spamming.")
        return
    await on_message_handler(bot, message)
    await bot.process_commands(message)


@bot.event
async def on_member_join(member):
    await on_member_join_handler(bot, member)


if __name__ == "__main__":
    bot.run(settings.DISCORD_BOT_TOKEN)

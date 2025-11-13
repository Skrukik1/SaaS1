from discord.ext import commands
from bot.utils.i18n import get_translation

general_commands = []


@general_commands.append
@commands.command(name="help")
async def help_command(ctx):
    help_text = await get_translation(ctx.guild.id, "help_text")
    await ctx.send(help_text)


@general_commands.append
@commands.command(name="info")
async def info_command(ctx):
    info = await get_translation(ctx.guild.id, "info_text")
    await ctx.send(info)


@general_commands.append
@commands.command(name="profile")
async def profile_command(ctx):
    # Placeholder: fetch user profile from backend API
    await ctx.send(await get_translation(ctx.guild.id, "profile_info", user=ctx.author.name))

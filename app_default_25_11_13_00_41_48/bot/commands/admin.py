from discord.ext import commands
from bot.utils.security import has_admin_permission
from bot.utils.i18n import get_translation

admin_commands = []


@commands.command(name="ban")
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: commands.MemberConverter, *, reason=None):
    if not await has_admin_permission(ctx.author):
        await ctx.send(await get_translation(ctx.guild.id, "error_no_permission"))
        return
    await member.ban(reason=reason)
    await ctx.send(await get_translation(ctx.guild.id, "user_banned", user=member.name))


@commands.command(name="unban")
@commands.has_permissions(ban_members=True)
async def unban(ctx, member_name: str):
    if not await has_admin_permission(ctx.author):
        await ctx.send(await get_translation(ctx.guild.id, "error_no_permission"))
        return
    banned_users = await ctx.guild.bans()
    member = None
    for ban_entry in banned_users:
        if ban_entry.user.name == member_name:
            member = ban_entry.user
            break
    if member is None:
        await ctx.send(await get_translation(ctx.guild.id, "user_not_found"))
        return
    await ctx.guild.unban(member)
    await ctx.send(await get_translation(ctx.guild.id, "user_unbanned", user=member_name))


@commands.command(name="clearcache")
async def clear_cache(ctx):
    if not await has_admin_permission(ctx.author):
        await ctx.send(await get_translation(ctx.guild.id, "error_no_permission"))
        return
    # Placeholder: clear cache logic
    await ctx.send(await get_translation(ctx.guild.id, "cache_cleared"))


admin_commands.extend([ban, unban, clear_cache])

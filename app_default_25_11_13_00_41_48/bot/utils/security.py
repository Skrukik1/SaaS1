import time
from discord.ext import commands

_spam_cache = dict()
_cooldowns = dict()


async def is_spam_message(message):
    user_id = message.author.id
    now = time.monotonic()
    times = _spam_cache.get(user_id, [])
    times = [t for t in times if now - t < 10]
    if len(times) >= 5:
        return True
    times.append(now)
    _spam_cache[user_id] = times
    return False


async def check_permissions(member, required_roles=None):
    if required_roles is None:
        return True
    member_roles = {role.name for role in member.roles}
    return bool(member_roles.intersection(set(required_roles)))


async def has_admin_permission(member):
    return await check_permissions(member, required_roles=["Admin", "Moderator"])


def command_cooldown(seconds):
    def decorator(func):
        async def wrapper(ctx, *args, **kwargs):
            user_id = ctx.author.id
            now = time.monotonic()
            last = _cooldowns.get(user_id, 0)
            if now - last < seconds:
                await ctx.send("You are on cooldown, please wait.")
                return
            _cooldowns[user_id] = now
            await func(ctx, *args, **kwargs)
        return wrapper
    return decorator

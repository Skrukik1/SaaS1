import aioredis
from app.config import settings

_redis_client = None


async def get_redis_client() -> aioredis.Redis:
    global _redis_client
    if _redis_client is None:
        _redis_client = await aioredis.from_url(settings.REDIS_URL, encoding="utf-8", decode_responses=True)
    return _redis_client


async def set_cache(key: str, value: str, expire: int = 300):
    redis = await get_redis_client()
    await redis.set(key, value, ex=expire)


async def get_cache(key: str):
    redis = await get_redis_client()
    return await redis.get(key)


async def invalidate_cache(key: str):
    redis = await get_redis_client()
    await redis.delete(key)

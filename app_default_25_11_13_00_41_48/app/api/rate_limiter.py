import time
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.status import HTTP_429_TOO_MANY_REQUESTS
from app.config import settings
import aioredis


class RateLimiterMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.redis = None

    async def dispatch(self, request: Request, call_next):
        if self.redis is None:
            self.redis = await aioredis.from_url(settings.REDIS_URL, encoding="utf-8", decode_responses=True)

        client_id = request.client.host or "anonymous"
        # Here key can be refined to include user id or API key if available
        key = f"rate_limit:{client_id}:{request.url.path}"
        limit = self._get_limit(request)

        try:
            current = await self.redis.get(key)
            if current is None:
                await self.redis.set(key, 1, ex=60)
                current = 1
            else:
                current = int(current)
                if current >= limit:
                    return JSONResponse(
                        status_code=HTTP_429_TOO_MANY_REQUESTS,
                        content={"detail": f"Rate limit exceeded: {limit} requests per minute"},
                    )
                else:
                    await self.redis.incr(key)
        except Exception:
            # If Redis is down, allow request to avoid service disruption
            pass

        response = await call_next(request)
        return response

    def _get_limit(self, request: Request) -> int:
        # Simplified: Admins get higher limit, others default limit
        # For demo, all get default limit
        try:
            limit_str = settings.RATE_LIMIT_DEFAULT
            num, per = limit_str.split("/")
            num = int(num)
            return num
        except Exception:
            return 100  # fallback

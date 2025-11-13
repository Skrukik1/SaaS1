from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from app.config import settings
from app.database import AsyncSessionLocal
from app.models.user import User
from app.utils.security import verify_password
from app.schemas.auth import TokenPayload

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_db_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session


async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db_session)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials"
    )
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=["HS256"])
        token_data = TokenPayload(**payload)
    except JWTError:
        raise credentials_exception

    user = await db.get(User, token_data.user_id)
    if not user:
        raise credentials_exception
    return user


def require_roles(required_roles: List[str]):
    async def role_checker(current_user: User = Depends(get_current_user)):
        user_roles = set(current_user.roles or [])
        if not user_roles.intersection(required_roles):
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return current_user

    return role_checker


async def get_cache_client():
    # Lazy import to prevent circular dependencies
    import aioredis
    redis = await aioredis.from_url(settings.REDIS_URL, encoding="utf-8", decode_responses=True)
    try:
        yield redis
    finally:
        await redis.close()

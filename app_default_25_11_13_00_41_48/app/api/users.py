from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional

from app.api.dependencies import get_db_session, require_roles
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.utils.security import hash_password
from app.utils.cache import invalidate_cache
from app.utils.logging import logger

router = APIRouter()


@router.get("", response_model=List[UserResponse])
async def list_users(
    db: AsyncSession = Depends(get_db_session),
    current_user=Depends(require_roles(["admin"])),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
):
    result = await db.execute(select(User).offset(skip).limit(limit))
    users = result.scalars().all()
    return users


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_in: UserCreate,
    db: AsyncSession = Depends(get_db_session),
    current_user=Depends(require_roles(["admin"])),
):
    existing = await db.execute(select(User).where(User.username == user_in.username))
    if existing.scalars().first():
        raise HTTPException(status_code=400, detail="Username already registered")
    user = User(
        username=user_in.username,
        email=user_in.email,
        roles=user_in.roles or [],
    )
    user.set_password(user_in.password)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    await invalidate_cache(f"user:{user.id}")
    logger.info(f"User {user.username} created by {current_user.username}")
    return user


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db_session),
    current_user=Depends(require_roles(["admin", "user"])),
):
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_in: UserUpdate,
    db: AsyncSession = Depends(get_db_session),
    current_user=Depends(require_roles(["admin"])),
):
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user_in.email:
        user.email = user_in.email
    if user_in.password:
        user.set_password(user_in.password)
    if user_in.roles is not None:
        user.roles = user_in.roles
    await db.commit()
    await db.refresh(user)
    await invalidate_cache(f"user:{user.id}")
    logger.info(f"User {user.username} updated by {current_user.username}")
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db_session),
    current_user=Depends(require_roles(["admin"])),
):
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    await db.delete(user)
    await db.commit()
    await invalidate_cache(f"user:{user.id}")
    logger.info(f"User {user.username} deleted by {current_user.username}")
    return None

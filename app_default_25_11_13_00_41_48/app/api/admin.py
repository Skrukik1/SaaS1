from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional

from app.api.dependencies import get_db_session, require_roles
from app.models.role import Role
from app.models.log import Log
from app.schemas.user import UserResponse
from app.utils.logging import logger

router = APIRouter()


@router.get("/roles", response_model=List[Role])
async def list_roles(
    db: AsyncSession = Depends(get_db_session),
    current_user=Depends(require_roles(["admin"])),
):
    result = await db.execute(select(Role))
    roles = result.scalars().all()
    return roles


@router.post("/roles", response_model=Role, status_code=status.HTTP_201_CREATED)
async def create_role(
    role: Role,
    db: AsyncSession = Depends(get_db_session),
    current_user=Depends(require_roles(["admin"])),
):
    existing = await db.execute(select(Role).where(Role.name == role.name))
    if existing.scalars().first():
        raise HTTPException(status_code=400, detail="Role name already exists")
    db.add(role)
    await db.commit()
    await db.refresh(role)
    logger.info(f"Role {role.name} created by {current_user.username}")
    return role


@router.put("/roles/{role_id}", response_model=Role)
async def update_role(
    role_id: int,
    role_update: Role,
    db: AsyncSession = Depends(get_db_session),
    current_user=Depends(require_roles(["admin"])),
):
    role = await db.get(Role, role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    role.name = role_update.name
    role.description = role_update.description
    role.permissions = role_update.permissions
    await db.commit()
    await db.refresh(role)
    logger.info(f"Role {role.name} updated by {current_user.username}")
    return role


@router.delete("/roles/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_role(
    role_id: int,
    db: AsyncSession = Depends(get_db_session),
    current_user=Depends(require_roles(["admin"])),
):
    role = await db.get(Role, role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    await db.delete(role)
    await db.commit()
    logger.info(f"Role {role.name} deleted by {current_user.username}")
    return None


@router.get("/logs", response_model=List[Log])
async def get_logs(
    level: Optional[str] = Query(None),
    source: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=200),
    db: AsyncSession = Depends(get_db_session),
    current_user=Depends(require_roles(["admin"])),
):
    query = select(Log)
    if level:
        query = query.where(Log.level == level)
    if source:
        query = query.where(Log.source == source)
    query = query.order_by(Log.timestamp.desc()).limit(limit)
    result = await db.execute(query)
    logs = result.scalars().all()
    return logs


@router.get("/settings")
async def get_settings(current_user=Depends(require_roles(["admin"]))):
    # Placeholder: Return app settings (fetch from config or DB)
    return {"rate_limit_default": settings.RATE_LIMIT_DEFAULT, "log_level": settings.LOG_LEVEL}


@router.put("/settings")
async def update_settings(
    data: dict,
    current_user=Depends(require_roles(["admin"])),
):
    # Placeholder: Update settings (persist to DB or config)
    # For demo, just echo back
    logger.info(f"Settings updated by {current_user.username}: {data}")
    return data

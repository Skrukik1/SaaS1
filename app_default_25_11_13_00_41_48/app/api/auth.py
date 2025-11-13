from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta
from jose import jwt
import uuid

from app.api.dependencies import get_db_session
from app.models.user import User
from app.schemas.auth import LoginRequest, TokenResponse
from app.utils.security import verify_password, create_access_token
from app.utils.logging import logger

router = APIRouter()


@router.post("/login", response_model=TokenResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db_session)):
    # form_data.username, form_data.password
    user = await db.execute(
        "SELECT * FROM users WHERE username = :username", {"username": form_data.username}
    )
    user_obj = user.scalar_one_or_none()
    if not user_obj:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    if not user_obj.verify_password(form_data.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")

    access_token_expires = timedelta(seconds=settings.JWT_ACCESS_TOKEN_EXPIRE_SECONDS)
    access_token = create_access_token(
        data={"user_id": user_obj.id, "roles": user_obj.roles}, expires_delta=access_token_expires
    )
    logger.info(f"User {user_obj.username} logged in.")
    return TokenResponse(access_token=access_token, expires_in=settings.JWT_ACCESS_TOKEN_EXPIRE_SECONDS)


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(current_user: User = Depends(get_db_session)):
    # For brevity, token refresh logic would be similar to login, with token validation
    # Here just a stub raising NotImplementedError for full implementation
    raise HTTPException(status_code=501, detail="Token refresh not implemented yet")


@router.post("/logout")
async def logout():
    # JWT stateless logout - could add token blacklist in Redis if required
    return {"message": "Logout successful"}

import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

from app.config import settings
from app.api.auth import router as auth_router
from app.api.users import router as users_router
from app.api.admin import router as admin_router
from app.api.middleware import ErrorHandlerMiddleware
from app.api.rate_limiter import RateLimiterMiddleware
from app.api.i18n import I18nMiddleware
from app.utils.logging import configure_logging

# Configure logging
configure_logging()

app = FastAPI(
    title="Comprehensive FastAPI Backend",
    description="Backend API with OAuth2 JWT authentication, RBAC, i18n, and more.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rate limiting middleware
app.add_middleware(RateLimiterMiddleware)

# I18n middleware
app.add_middleware(I18nMiddleware)

# Centralized error handling middleware
app.add_middleware(ErrorHandlerMiddleware)

# Mount static frontend files
app.mount("/static", StaticFiles(directory="frontend/build/static"), name="static")

# Include routers
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(users_router, prefix="/users", tags=["Users"])
app.include_router(admin_router, prefix="/admin", tags=["Admin"])

# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok"}

# Root endpoint redirecting to docs
@app.get("/", include_in_schema=False)
async def root():
    return {"message": "Welcome to the API. Visit /docs for API documentation."}

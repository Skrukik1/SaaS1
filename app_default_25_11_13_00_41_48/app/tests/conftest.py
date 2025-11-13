import pytest
import asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base
from app.config import settings
import aioredis
from unittest.mock import AsyncMock

DATABASE_TEST_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def db_engine():
    engine = create_async_engine(DATABASE_TEST_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest.fixture
async def db_session(db_engine):
    async_session = sessionmaker(db_engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session


@pytest.fixture
async def client(db_session):
    async with AsyncClient(app=app, base_url="http://testserver") as ac:
        yield ac


@pytest.fixture
async def redis_mock(monkeypatch):
    mock = AsyncMock()
    monkeypatch.setattr("app.utils.cache.get_redis_client", lambda: asyncio.Future())
    monkeypatch.setattr("app.utils.cache.get_redis_client", lambda: mock)
    yield mock


@pytest.fixture
async def discord_bot_mock(monkeypatch):
    mock = AsyncMock()
    yield mock

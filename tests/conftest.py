import os
# GARANTE ISOLAMENTO AUTOMÁTICO
os.environ["ENVIRONMENT"] = "test"

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from src.database.base import Base
from src.database.session import get_db
from src.main import app


TEST_DATABASE_URL = "sqlite+aiosqlite:///./db_test_pytest.sqlite"

engine = create_async_engine(TEST_DATABASE_URL)

TestingSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)


# =========================
# DB SETUP / TEARDOWN
# =========================
@pytest_asyncio.fixture(scope="function")
async def db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with TestingSessionLocal() as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all) # se comentar consegue ver os dados do banco de teste


# =========================
# OVERRIDE DEPENDENCY
# =========================
@pytest_asyncio.fixture(scope="function")
async def override_get_db(db):
    async def _get_db():
        yield db

    app.dependency_overrides[get_db] = _get_db
    yield
    app.dependency_overrides.clear()


# =========================
# CLIENTE HTTP
# =========================
@pytest_asyncio.fixture(scope="function")
async def client(override_get_db):
    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test"
    ) as client:
        yield client

from typing import AsyncGenerator, Any

import pytest_asyncio

from sqlalchemy.ext.asyncio import AsyncSession

from app.settings import settings
from app.database_settings import DatabaseManager
from tests.db_helper import create_temp_api_key_usage
from app.models import APIKeyUsage


TEST_DATABASE_URL: str = settings.TEST_DATABASE_URL
BROKEN_DATABASE_URL = (
    "postgresql+asyncpg://wrong_user:wrong_pass@localhost:9999/bad_db"
)


@pytest_asyncio.fixture
async def db_manager() -> AsyncGenerator[DatabaseManager, Any]:
    """database manger class with test database url

    Returns:
        AsyncGenerator[DatabaseManager, Any]: database manager class

    Yields:
        Iterator[AsyncGenerator[DatabaseManager, Any]]: database manager class
    """
    db = DatabaseManager(TEST_DATABASE_URL)
    db.initialize()
    yield db
    await db.dispose()


@pytest_asyncio.fixture
async def broken_db(
) -> AsyncGenerator[DatabaseManager, Any]:
    """database manger class with broken url

    Returns:
        AsyncGenerator[DatabaseManager, Any]: database manger class.

    Yields:
        Iterator[AsyncGenerator[DatabaseManager, Any]]:  database manger class.
    """
    db = DatabaseManager(BROKEN_DATABASE_URL)
    db.initialize()
    yield db
    await db.dispose()


@pytest_asyncio.fixture
async def broken_db_session(broken_db: DatabaseManager) -> AsyncGenerator[AsyncSession, Any]:
    """this an broken db session

    Args:
        broken_db (DatabaseManager): database class

    Returns:
        AsyncGenerator[AsyncSession, Any]: session

    Yields:
        Iterator[AsyncGenerator[AsyncSession, Any]]: session
    """
    async with broken_db.session() as session:
        yield session


@pytest_asyncio.fixture
async def db_session(db_manager: DatabaseManager) -> AsyncGenerator[AsyncSession, Any]:
    """Yields a clean DB session for each test.

    Args:
        db_manager (DatabaseManager): database manger class

    Returns:
        AsyncGenerator[AsyncSession, Any]: yield session

    Yields:
        Iterator[AsyncGenerator[AsyncSession, Any]]: session
    """
    async with db_manager.session() as session:
        yield session


@pytest_asyncio.fixture
async def temp_api_key(db_session: AsyncSession) -> AsyncGenerator[APIKeyUsage, Any]:
    """yield a ApiKeyUsage Object for Test Cases.

    Args:
        db_session (AsyncSession): database session

    Yields:
        APIKeyUsage: APIKeyUsage object 
    """
    async with create_temp_api_key_usage(db_session) as api_key:
        yield api_key

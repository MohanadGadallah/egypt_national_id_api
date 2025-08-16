from contextlib import asynccontextmanager
from typing import AsyncGenerator
import logging

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine, async_sessionmaker
import sqlalchemy as sa
import sqlalchemy.orm as so
from app.settings import settings


logger = logging.getLogger(__name__)


class DatabaseManager:
    def __init__(self, database_url: str):
        self._engine: AsyncEngine | None = None
        self._session_factory = None
        self._database_url = database_url

    def initialize(self) -> None:
        self._engine = create_async_engine(self._database_url)
        self._session_factory = async_sessionmaker(
            self._engine, expire_on_commit=False, class_=AsyncSession)
        logger.info("Database engine initialized")

    @asynccontextmanager
    async def session(self) -> AsyncGenerator[AsyncSession, None]:
        session = self._session_factory()
        try:
            yield session
        except Exception:
            await session.rollback()
            logger.error("Session rollback due to exception")
            raise
        finally:
            await session.close()

    async def validate_connection(self) -> None:
        async with self.session() as session:
            await session.execute(sa.text("SELECT 1"))
        logger.info("Database connection validated")

    async def dispose(self) -> None:
        """Dispose of the engine."""
        if self._engine:
            await self._engine.dispose()
            logger.info("Database engine disposed")
            self._engine = None
            self._session_factory = None


DB_MANAGER = DatabaseManager(settings.DATABASE_URL)


class Base(so.DeclarativeBase):
    pass


async def db_session():
    async with DB_MANAGER.session() as session:
        yield session
        await session.close()

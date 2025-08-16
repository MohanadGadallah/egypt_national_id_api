from typing import AsyncGenerator
from contextlib import asynccontextmanager
from datetime import datetime, timezone

from app.models import APIKeyUsage

from sqlalchemy.sql import text
from sqlalchemy.ext.asyncio import AsyncSession

API_KEY: str = "test"


@asynccontextmanager
async def temporarily_rename_table(
    session: AsyncSession, old_name: str, temp_name: str
):
    """
    you must rollback session.

    Args:
        session (AsyncSession):ready to act session.
        old_name (str): table old name.
        temp_name (str): table new name.

    Yields:
        _type_: session object yileded ypu must rollback
    """
    try:
        await session.execute(
            text(f'ALTER TABLE "{old_name}" RENAME TO {temp_name}')
        )
        await session.commit()

        yield session
        await session.execute(
            text(f'ALTER TABLE "{old_name}" RENAME TO {temp_name}')
        )
        await session.commit()
    except Exception:
        await session.rollback()

    finally:
        await session.execute(
            text(f'ALTER TABLE {temp_name} RENAME TO "{old_name}"')
        )
        await session.commit()


@asynccontextmanager
async def create_temp_api_key_usage(session: AsyncSession) -> AsyncGenerator[APIKeyUsage, None]:
    """
    Async context manager to create a temporary APIKeyUsage record in the DB,
    and automatically delete it after usage.
    """
    api_key_usage = APIKeyUsage(
        company_name="Test Company",
        api_key=API_KEY,
        usage_count=0,
        last_request_at=datetime.now(timezone.utc)
    )

    session.add(api_key_usage)
    await session.commit()
    await session.refresh(api_key_usage)

    try:
        yield api_key_usage
    finally:
        await session.delete(api_key_usage)
        await session.commit()

import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.database_operations import validate_api_key
from tests.db_helper import temporarily_rename_table, API_KEY
from app.models import APIKeyUsage


@pytest.mark.asyncio
async def test_validate_api_key(db_session: AsyncSession, temp_api_key: APIKeyUsage) -> None:
    """ success test case with valid api key 

    Args:
        db_session (AsyncSession): database session.
        temp_api_key (APIKeyUsage): DI object for test case.
    """
    result = await validate_api_key(db_session, API_KEY)
    assert result


@pytest.mark.asyncio
async def test_validate_api_key_invalid_key(db_session: AsyncSession, temp_api_key: APIKeyUsage) -> None:
    result = await validate_api_key(db_session, "gg")
    assert result is False


@pytest.mark.asyncio
async def test_validate_api_key_with_broken_db(broken_db_session: AsyncSession, temp_api_key: APIKeyUsage) -> None:
    result = await validate_api_key(broken_db_session, API_KEY)
    assert result is False


@pytest.mark.asyncio
async def test_validate_api_key_with_broken_db_table(db_session: AsyncSession, temp_api_key: APIKeyUsage) -> None:
    async with temporarily_rename_table(
        db_session, old_name="ApiKeyUsages", temp_name="ApiKeyUsages_backup"
    ) as session:
        result = await validate_api_key(session, API_KEY)
        assert result is False

import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
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
    """test case with invalid api key

    Args:
        db_session (AsyncSession): db session
        temp_api_key (APIKeyUsage): DI object for test case.
    """

    with pytest.raises(HTTPException) as code:
        await validate_api_key(db_session, "gg")
    assert code.value.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_validate_api_key_with_broken_db(broken_db_session: AsyncSession, temp_api_key: APIKeyUsage) -> None:
    """test case with wrong database url

    Args:
        broken_db_session (AsyncSession):  db session
        temp_api_key (APIKeyUsage):  DI object for test case.
    """
    with pytest.raises(HTTPException) as code:
        await validate_api_key(broken_db_session, API_KEY)
    assert code.value.status_code == status.HTTP_503_SERVICE_UNAVAILABLE


@pytest.mark.asyncio
async def test_validate_api_key_with_broken_db_table(db_session: AsyncSession, temp_api_key: APIKeyUsage) -> None:
    """test case with wrong database table 

    Args:
        broken_db_session (AsyncSession):  db session
        temp_api_key (APIKeyUsage):  DI object for test case.
    """
    async with temporarily_rename_table(
        db_session, old_name="ApiKeyUsages", temp_name="ApiKeyUsages_backup"
    ) as session:
        with pytest.raises(HTTPException) as code:
            await validate_api_key(session, API_KEY)
        assert code.value.status_code == status.HTTP_503_SERVICE_UNAVAILABLE

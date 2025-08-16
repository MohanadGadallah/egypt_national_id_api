import logging
from datetime import datetime, timezone

import sqlalchemy as sa
from sqlalchemy.exc import DBAPIError, OperationalError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import APIKeyUsage

logger: logging.Logger = logging.getLogger(__name__)


async def validate_api_key(db_session: AsyncSession, api_key: str) -> bool:
    """
    Validates an API key and atomically increments its usage count with row level locking.

    Args:
        db_session (AsyncSession): Database session.
        api_key (str): API key to validate.

    Returns:
        bool: `True`if key is valid and updated, `False` otherwise.
    """
    try:
        query = (
            sa.select(APIKeyUsage)
            .where(APIKeyUsage.api_key == api_key)
            .with_for_update()
        )

        result = await db_session.execute(query)

        if row := result.scalars().first():
            row.usage_count += 1
            row.last_request_at = datetime.now(timezone.utc)

            await db_session.commit()

            logger.info(
                "[validate_api_key] (%s) company has used the key", row.company_name)
            return True

        logger.error("[validate_api_key] : no key found")
        return False

    except (OperationalError, DBAPIError) as database_error:
        await db_session.rollback()
        logger.error("[validate_api_key] database error (%s)", database_error)
        return False
    except Exception as except_error:
        logger.critical(
            "[unhandled_database_error] at validate_api_key error (%s)", except_error)
        return False

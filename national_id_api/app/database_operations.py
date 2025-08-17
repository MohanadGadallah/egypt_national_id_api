import logging
from datetime import datetime, timezone

from fastapi import status, HTTPException

import sqlalchemy as sa
from sqlalchemy.exc import DBAPIError, OperationalError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import APIKeyUsage
from app.response_codes import ErrorCodeEnum

logger: logging.Logger = logging.getLogger(__name__)


async def validate_api_key(db_session: AsyncSession, api_key: str) -> bool:
    """
    Validates an API key and atomically increments its usage count with row level locking.

    Raises:
        HTTPException: with 401 if the key is invalid,
                       503 if there id a DB or unknown error.

    Returns:
        True if the key is valid.
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
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "data": None,
                "message": "Unauthorized Access. Thanks for using TRU National ID Service",
                "code": ErrorCodeEnum.UNAUTHORIZED.value,
            },
        )

    except HTTPException:
        raise
    except (OperationalError, DBAPIError) as db_error:
        await db_session.rollback()
        logger.error("[validate_api_key] database error: %s", db_error)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "data": None,
                "message": "Service temporarily unavailable. Please try again later.",
                "code": ErrorCodeEnum.SERVICE_UNAVAILABLE.value,
            },
        ) from db_error

    except Exception as unexpected_error:
        await db_session.rollback()
        logger.critical(
            "[validate_api_key] unexpected error: %s", unexpected_error)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "data": None,
                "message": "Service temporarily unavailable due to an internal error.",
                "code": ErrorCodeEnum.SERVICE_UNAVAILABLE.value,
            },
        ) from unexpected_error

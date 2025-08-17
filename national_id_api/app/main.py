import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status, Header, Depends, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded

from sqlalchemy.ext.asyncio import AsyncSession

from app.schema import InputID
from app.response_codes import SuccessCodeEnum, ErrorCodeEnum
from app.national_id import NationalID
from app.database_settings import DB_MANAGER, db_session
from app.database_operations import validate_api_key
from app.custom_exceptions import (
    http_exception_handler,
    validation_exception_handler,
    custom_rate_limit_handler,
)

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["10/minute"],
    storage_uri="memory://",
    strategy="fixed-window"
)


logger: logging.Logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """ startup and shut down events

    """

    DB_MANAGER.initialize()

    try:
        await DB_MANAGER.validate_connection()
        logger.info(" Connected to the database")
    except Exception as e:
        logger.critical(
            " Failed to connect to the database during startup: %s", e)

    yield

    try:
        await DB_MANAGER.dispose()
        logger.info(" Database connection disposed")
    except Exception as e:
        logger.warning("Failed to dispose DB engine: %s", e)

app = FastAPI(lifespan=lifespan)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(RateLimitExceeded, custom_rate_limit_handler)
app.add_middleware(SlowAPIMiddleware)
app.state.limiter = limiter

# API


async def verify_api_key(x_api_key: str = Header(None), session: AsyncSession = Depends(db_session)) -> bool | JSONResponse:
    """_summary_

    Args:
        x_api_key (str): service api key .
        session (AsyncSession): database session. Defaults to Depends(db_session).

    Returns:
        bool: `True` if it's right also it autoincrement usage, `false`  otherwise 
    """
    try:
        return await validate_api_key(db_session=session, api_key=x_api_key)
    except Exception as except_error:
        logger.critical(
            "[unhandled_error] at verify_api_key error (%s) ", except_error)
        raise


@app.post("/validate-id")
@limiter.limit("100/minute")
@limiter.limit("5/second")
async def validate_national_id(data: InputID, request: Request, valid_key: str = Depends(verify_api_key),):
    """
    Validates the provided Egyptian National ID.

    The National ID must:
    - Be exactly 14 digits long.
    - Contain only numeric characters.

    Returns:
        JSONResponse: A structured response indicating whether the ID is valid,
                      along with extracted data and a message.
    """
    try:

        national_id = NationalID(id_number=str(data.national_id))
        logger.info("Validation completed. Result: %s",
                    "Valid" if national_id.is_valid else "Fake")
        if national_id.is_valid:
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "data": national_id.__dict__,
                    "message": " Valid ID .thanks for using TRU National ID Service",
                    "code": SuccessCodeEnum.VALID_ID.value
                }
            )
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "data": national_id.__dict__,
                "message": "Invalid ID .Thanks for using TRU National ID Service",
                "code": ErrorCodeEnum.INVALID_ID.value
            }
        )
    except Exception as except_error:
        logger.critical("unhandled exception error: %s", except_error)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "data": None,
                "message": "Something went wrong! .Thanks for using TRU National ID Service",
                "code": ErrorCodeEnum.SOMETHING_WENT_WRONG.value
            }
        )

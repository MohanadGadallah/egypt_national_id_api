
import logging

from fastapi import Request, status,  HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from slowapi.errors import RateLimitExceeded

from app.response_codes import ErrorCodeEnum

logger: logging.Logger = logging.getLogger(__name__)


async def http_exception_handler(request: Request, exc: HTTPException):
    logger.error(f"HTTPException: {exc.detail}")

    if isinstance(exc.detail, dict):
        return JSONResponse(
            status_code=exc.status_code,
            content=exc.detail
        )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "data": None,
            "message": f"An error occurred: {str(exc.detail)}",
            "code": ErrorCodeEnum.SOMETHING_WENT_WRONG.value,
        }
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """_summary_

    Args:
        request (Request): _description_
        exc (RequestValidationError): _description_

    Returns:
        _type_: _description_
    """
    logger.error(f"Validation failed: {str(exc.body)}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "data": None,
            "message": f"Validation failed: {str(exc.body)}",
            "code": ErrorCodeEnum.PARSING_ERROR.value,
        }
    )


async def custom_rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        content={
            "data": None,
            "message": "Too many requests. Please wait and try again.",
            "code": ErrorCodeEnum.TOO_MANY_REQUEST.value
        }
    )

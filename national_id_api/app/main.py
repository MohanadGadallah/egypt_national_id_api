import logging
from fastapi import FastAPI,Request,HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.schema import InputID
from app.national_id import NationalID

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


logger :logging.Logger= logging.getLogger(__name__)

app = FastAPI(title="test")



app = FastAPI()



@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
    """_summary_

    Args:
        request (Request): _description_
        exc (StarletteHTTPException): _description_

    Returns:
        _type_: _description_
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "data": None,
            "message": f"An error occurred: {exc.detail}",
            "code": "ErrorCodeEnum.SERVER_ERROR.value",
        }
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """_summary_

    Args:
        request (Request): _description_
        exc (RequestValidationError): _description_

    Returns:
        _type_: _description_
    """
    return JSONResponse(
        status_code=422,  
        content={
            "data": None,
            "message":f"Validation failed: {str(exc.body)}",
            "code": "ErrorCodeEnum.PARSING_ERROR.value",
        }
    )


@app.post("/")
async def test_endpoint(data:InputID,request:Request):
    """_summary_

    Returns:
        _type_: _description_
    """
    national_id = NationalID(id_number=data.national_id)
    national_id.validate_century()
    national_id.validate_year()
    logger.info("test done ")
    logger.error("ddd")
    logger.critical("gggg")
    logger.debug("dd")
    return {"message": national_id.year_of_birth}


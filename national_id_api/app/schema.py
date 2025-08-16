from typing import Annotated
from decimal import Decimal
from pydantic import BaseModel,Field
from pydantic import BaseModel, Field, ValidationError,field_validator
from typing import Annotated
from decimal import Decimal
from enum import Enum


class ErrorCodeEnum(Enum):
    INVALID_ID = "INVALID_ID"
    INVALID_LENGTH = "INVALID_LENGTH"
    OUT_OF_RANGE = "OUT_OF_RANGE"

class ErrorResponse(BaseModel):
    data: dict | None = None
    message: str
    code: ErrorCodeEnum
    
    
class InputID(BaseModel):
    """_summary_

    Args:
        BaseModel (_type_): _description_
    """
    national_id: Annotated[
        Decimal,Field(ge=10000000000000, le=99999999999999)]
    

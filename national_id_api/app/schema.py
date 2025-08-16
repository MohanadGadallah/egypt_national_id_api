from typing import Annotated
from decimal import Decimal
from pydantic import BaseModel,Field


class InputID(BaseModel):
    """_summary_

    Args:
        BaseModel (_type_): _description_
    """
    national_id: Annotated[
        Decimal,Field(ge=10000000000000, le=99999999999999)]
    


from typing import Optional
from enum import Enum
from dataclasses import dataclass

class Governorates(Enum):
    """_summary_

    Args:
        Enum (_type_): _description_
    """
    CAIRO = 1
    ALEXANDRIA = 2
    PORT_SAID = 3
    SUEZ = 4
    DAMIETTA = 11
    DAKAHLIA = 12
    SHARQIA = 13


@dataclass
class NationalID:
    """_summary_
    """
    id_number: str
    is_valid:bool=False
    year_of_birth: Optional[int] = None
    month_of_birth: Optional[int] = None
    day_of_birth: Optional[int] = None
    governorate_id: Optional[str] = None
    governorate_name:Optional[int]=None
    unique_num: Optional[int] = None
    century: Optional[int] = None
    verification_digit: Optional[int] = None
    
    
    
    def _validate_length_and_digits(self) -> bool:
        """The Egyptian national ID number contains 14 digits.

        Returns:
            bool: True if the ID number is valid based on the format, False otherwise.
        """
        return len(self.id_number) == 14 and self.id_number.isdigit()
    
    
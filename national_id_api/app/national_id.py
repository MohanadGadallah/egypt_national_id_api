from typing import Optional
from enum import Enum
from datetime import datetime
import calendar
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
    QALYUBIA = 14
    KAFR_EL_SHEIKH = 15
    GHARBIA = 16
    MONUFIA = 17
    BEHEIRA = 18
    ISMAILIA = 19
    GIZA = 21
    BENI_SUEF = 22
    FAYOUM = 23
    MINYA = 24
    ASYUT = 25
    SOHAG = 26
    QENA = 27
    ASWAN = 28
    LUXOR = 29
    RED_SEA = 31
    NEW_VALLEY = 32
    MATRUH = 33
    NORTH_SINAI = 34
    SOUTH_SINAI = 35
    OUTSIDE_THE_REPUBLIC = 88

@dataclass
class NationalID:
    """_summary_
    """
    id_number: str
    is_valid:bool=False
    year_of_birth: Optional[int] = None
    month_of_birth: Optional[int] = None
    month_of_birth_name: Optional[str] = None
    day_of_birth: Optional[int] = None
    gender:Optional[str]=None
    governorate_id: Optional[int] = None
    governorate_name:Optional[str]=None
    unique_num: Optional[int] = None
    century: Optional[int] = None
    verification_digit: Optional[int] = None
    
    
    def __post_init__(self):
        """_summary_

        Raises:
            ValueError: _description_
        """
        if not self.validate_length_and_digits():
            raise ValueError(f"Invalid National ID number: {self.id_number}")
    def validate_length_and_digits(self) -> bool:
        """The Egyptian national ID number contains 14 digits.

        Returns:
            bool: True if the ID number is valid based on the format, False otherwise.
        """
        self.id_number=str(self.id_number)
        if len(self.id_number) == 14 and self.id_number.isdigit():
            return True
        return False
    
    def validate_century(self) -> bool:
        """_summary_

        Returns:
            bool: _description_
        """
        self.century = int(self.id_number[0])
        if self.century in [2, 3]:
            return True
        return False
    
    def validate_year(self) -> bool:
        """Validates if the year part of the ID is not in the future

        Returns:
            bool: _description_
        """
        
        self.year_of_birth = int(self.id_number[1:3])  
        current_year = datetime.now().year


        if self.century == 2:
            full_year = 1900 + self.year_of_birth  
        elif self.century == 3:
            full_year = 2000 + self.year_of_birth  
        else:
            full_year = self.year_of_birth  

        if full_year > current_year:
            return False  
        self.year_of_birth=full_year
        return True
    def validate_month(self) -> bool:
        """validates the month part of the ID (1 to 12)

        Returns:
            bool: _description_
        """
        self.month_of_birth = int(self.id_number[3:5])
        if self.month_of_birth in range(1, 13):
            self.month_of_birth_name = calendar.month_name[self.month_of_birth]
            return True
        
        return False
    def validate_day(self) -> bool:
        """_summary_

        Returns:
            bool: _description_
        """
        self.day_of_birth = int(self.id_number[5:7])
        if self.month_of_birth in [1, 3, 5, 7, 8, 10, 12]:
            return self.day_of_birth in range(1, 32)
        elif self.month_of_birth in [4, 6, 9, 11]:
            return self.day_of_birth in range(1, 31)
        elif self.month_of_birth == 2:
            if self.year_of_birth % 4 == 0:
                return self.day_of_birth in range(30) 
            else:
                return self.day_of_birth in range(29)
        return False
    def validate_governorate(self) -> bool:
        self.governorate_id = int(self.id_number[7:9])
        for governorate in Governorates:
            if governorate.value == self.governorate_id:
                self.governorate_name = governorate.name.capitalize().replace("_"," ")
                return True
        return False
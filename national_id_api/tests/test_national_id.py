import pytest
from app.national_id import NationalID

VAILD_ID_NUMBER: str = "29905228800910"


def test_valid_id() -> None:
    """ success test case for all.
    """
    valid_id: NationalID = NationalID(id_number=VAILD_ID_NUMBER)
    assert valid_id.id_number == VAILD_ID_NUMBER
    assert valid_id.is_valid is True
    assert valid_id.fake_id_reason == ""
    assert valid_id.year_of_birth == 1999
    assert valid_id.month_of_birth == 5
    assert valid_id.month_of_birth_name == "May"
    assert valid_id.day_of_birth == 22
    assert valid_id.gender == "Male"
    assert valid_id.governorate_name == "Outside the republic"


def test_invalid_length() -> None:
    """ check length and if it's a digit.
    """
    invalid_id: NationalID = NationalID(id_number="2123456789012")
    assert invalid_id.is_valid is False
    assert "invalid length or non numeric string" in str(
        invalid_id.fake_id_reason)


def test_invalid_century() -> None:
    """ check century 2 or 3. no other options.
    """
    invalid_id: NationalID = NationalID(id_number="41234567890123")
    assert invalid_id.is_valid is False
    assert "invalid century part" in str(invalid_id.fake_id_reason)


def test_future_year() -> None:
    """fake id year of birth check """
    future_id: NationalID = NationalID(id_number="33035000000000")
    assert future_id.is_valid is False
    assert future_id.year_of_birth == 2030
    assert "Year of birth is in the future" in str(future_id.fake_id_reason)


def test_invalid_month() -> None:
    """must be in range 1 to 12 
    """
    invalid_month_id: NationalID = NationalID(id_number="21213167890123")
    assert invalid_month_id.is_valid is False
    assert "invalid month" in str(invalid_month_id.fake_id_reason)


def test_invalid_day() -> None:
    """ checking days with year and month.
    """
    invalid_day_id: NationalID = NationalID(id_number="21230231234567")
    assert invalid_day_id.is_valid is False
    assert "invalid day for the month" in str(invalid_day_id.fake_id_reason)


def test_invalid_governorate() -> None:
    """check governorate if it's included or not (fake id).
    """
    invalid_governorate_id = NationalID(id_number="21239999999999")
    assert invalid_governorate_id.is_valid is False
    assert "invalid governorate ID" in str(
        invalid_governorate_id.fake_id_reason)


def test_gender_validation() -> None:
    """check wether the person is a female or a male.
    """
    male_id = NationalID(id_number="21234567891111")
    assert male_id.gender == "Male"

    female_id = NationalID(id_number="123456789012")
    assert female_id.gender == "Female"


def test_leap_year() -> None:
    """check leap year.
    """
    leap_year_id = NationalID(id_number="21202299000000")
    assert leap_year_id.day_of_birth == 29


def test_non_leap_year() -> None:
    """ check non leap year
    """
    non_leap_year_id = NationalID(id_number="21202319000000")
    assert non_leap_year_id.is_valid is False
    assert "invalid day for the month" in str(non_leap_year_id.fake_id_reason)

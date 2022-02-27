from typing import Optional

from pydantic import BaseModel, EmailStr, constr, validator

from app.models.contact import GroupTags
from phonenumbers import (
    NumberParseException,
    PhoneNumberFormat,
    PhoneNumberType,
    format_number,
    is_valid_number,
    number_type,
)
from phonenumbers import parse as parse_phone_number

MOBILE_NUMBER_TYPES = PhoneNumberType.MOBILE, PhoneNumberType.FIXED_LINE_OR_MOBILE


# Shared properties
class ContactBase(BaseModel):
    name: constr(max_length=60, strip_whitespace=True)
    description: constr(max_length=100, strip_whitespace=True) = None
    email: Optional[EmailStr] = None
    phone_number: constr(max_length=50, strip_whitespace=True)
    group_tag: GroupTags = GroupTags.UNDEFINED
    deleted: Optional[bool] = False

    @validator("phone_number")
    def check_phone_number(cls, value: str) -> str:
        """
        Method that uses the phonenumbers library to validate an incoming phone number string.
        Docs: https://github.com/daviddrysdale/python-phonenumbers
        """
        if value is None:
            return value

        try:
            # we're in Brazil, hence using "BR" as the default
            # and excluding country code for Brazilian numbers.
            number = parse_phone_number(value, "BR")
        except NumberParseException as exc:
            raise ValueError("Please provide a valid mobile phone number") from exc

        if not (is_valid_number(number) and number_type(number) in MOBILE_NUMBER_TYPES):
            raise ValueError("Please provide a valid mobile phone number")

        return format_number(
            number,
            PhoneNumberFormat.NATIONAL
            if number.country_code == 55  # Brazilian code
            else PhoneNumberFormat.INTERNATIONAL,
        )

    class Config:
        orm_mode = True
        use_enum_values = True


# Properties to receive on contact creation
class ContactCreate(ContactBase):
    name: constr(max_length=60, strip_whitespace=True)
    phone_number: constr(max_length=50, strip_whitespace=True)

    class Config:
        orm_mode = True


# Properties to receive on contact update
class ContactUpdate(ContactBase):
    name: constr(max_length=60, strip_whitespace=True) = None
    phone_number: constr(max_length=50, strip_whitespace=True) = None

    class Config:
        orm_mode = True


# Properties shared by models stored in DB
class ContactInDBBase(ContactBase):
    id: int
    name: constr(max_length=60, strip_whitespace=True)
    owner_id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Contact(ContactInDBBase):
    pass


# Properties properties stored in DB
class ContactInDB(ContactInDBBase):
    pass

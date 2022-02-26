import re
from typing import Optional

from pydantic import BaseModel, EmailStr, validator


# Shared properties
class ContactBase(BaseModel):
    name: str
    description: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: str
    group_tag: Optional[str] = None
    deleted: Optional[bool] = False

    @validator("phone_number")
    def phone_validation(cls, value) -> str:
        regex = r"^(\+)[1-9][0-9\-\(\)\.]{9,15}$"

        if value and not re.search(regex, value, re.I):
            raise ValueError("The informed phone number is invalid.")
        return value

    class Config:
        orm_mode = True
        use_enum_values = True


# Properties to receive on contact creation
class ContactCreate(ContactBase):
    pass


# Properties to receive on contact update
class ContactUpdate(ContactBase):
    pass


# Properties shared by models stored in DB
class ContactInDBBase(ContactBase):
    id: int
    name: str
    owner_id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Contact(ContactInDBBase):
    pass


# Properties properties stored in DB
class ContactInDB(ContactInDBBase):
    pass

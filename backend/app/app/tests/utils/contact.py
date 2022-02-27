from random import randint
from typing import Optional

from sqlalchemy.orm import Session

from app import crud, models
from app.schemas.contact import ContactCreate
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_lower_string
from phonenumbers import PhoneNumber, PhoneNumberFormat, format_number
from phonenumbers import parse as parse_phone_number


def random_phone_number(size: int = 8) -> str:
    range_start = 10 ** (size - 1)
    range_end = (10 ** size) - 1

    number_as_str = str(randint(range_start, range_end))

    return f"+55489{number_as_str}"


def format_phone_number(phone_number: PhoneNumber) -> str:
    if isinstance(phone_number, str):
        number = parse_phone_number(phone_number, "BR")
    else:
        number = phone_number

    return format_number(
        number,
        PhoneNumberFormat.NATIONAL
        if number.country_code == 55  # Brazilian code
        else PhoneNumberFormat.INTERNATIONAL,
    )


def create_random_contact(
    db: Session, *, owner_id: Optional[int] = None
) -> models.Contact:
    if owner_id is None:
        user = create_random_user(db)
        owner_id = user.id

    name = random_lower_string()
    description = random_lower_string()
    phone_number = random_phone_number()
    email = "what@ever.com"
    group_tag = models.contact.GroupTags.PERSONAL.value

    contact_in = ContactCreate(
        name=name,
        description=description,
        phone_number=phone_number,
        email=email,
        group_tag=group_tag,
        id=id,
    )

    return crud.contact.create_with_owner(db=db, obj_in=contact_in, owner_id=owner_id)

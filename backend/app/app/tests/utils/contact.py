from typing import Optional

from sqlalchemy.orm import Session

from app import crud, models
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_lower_string
from backend.app.app.schemas.contact import ContactCreate


def create_random_contact(
    db: Session, *, owner_id: Optional[int] = None
) -> models.Contact:
    if owner_id is None:
        user = create_random_user(db)
        owner_id = user.id

    title = random_lower_string()
    description = random_lower_string()
    contact_in = ContactCreate(title=title, description=description, id=id)

    return crud.contact.create_with_owner(db=db, obj_in=contact_in, owner_id=owner_id)

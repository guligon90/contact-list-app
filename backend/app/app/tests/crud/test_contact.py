from sqlalchemy.orm import Session

from app import crud
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_lower_string
from backend.app.app.schemas.contact import ContactCreate, ContactUpdate


def test_create_contact(db: Session) -> None:
    title = random_lower_string()
    description = random_lower_string()
    contact_in = ContactCreate(title=title, description=description)
    user = create_random_user(db)
    contact = crud.contact.create_with_owner(db=db, obj_in=contact_in, owner_id=user.id)

    assert contact.title == title
    assert contact.description == description
    assert contact.owner_id == user.id


def test_get_contact(db: Session) -> None:
    title = random_lower_string()
    description = random_lower_string()
    contact_in = ContactCreate(title=title, description=description)
    user = create_random_user(db)
    contact = crud.contact.create_with_owner(db=db, obj_in=contact_in, owner_id=user.id)
    stored_contact = crud.contact.get(db=db, id=contact.id)

    assert stored_contact
    assert contact.id == stored_contact.id
    assert contact.title == stored_contact.title
    assert contact.description == stored_contact.description
    assert contact.owner_id == stored_contact.owner_id


def test_update_contact(db: Session) -> None:
    title = random_lower_string()
    description = random_lower_string()
    contact_in = ContactCreate(title=title, description=description)
    user = create_random_user(db)
    contact = crud.contact.create_with_owner(db=db, obj_in=contact_in, owner_id=user.id)
    description2 = random_lower_string()
    contact_update = ContactUpdate(description=description2)
    contact2 = crud.contact.update(db=db, db_obj=contact, obj_in=contact_update)

    assert contact.id == contact2.id
    assert contact.title == contact2.title
    assert contact2.description == description2
    assert contact.owner_id == contact2.owner_id


def test_delete_contact(db: Session) -> None:
    title = random_lower_string()
    description = random_lower_string()
    contact_in = ContactCreate(title=title, description=description)
    user = create_random_user(db)
    contact = crud.contact.create_with_owner(db=db, obj_in=contact_in, owner_id=user.id)
    contact2 = crud.contact.remove(db=db, id=contact.id)
    contact3 = crud.contact.get(db=db, id=contact.id)

    assert contact3 is None
    assert contact2.id == contact.id
    assert contact2.title == title
    assert contact2.description == description
    assert contact2.owner_id == user.id

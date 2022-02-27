import pytest
from sqlalchemy.orm import Session

from app import crud
from app.api.api_v1.exceptions.contacts import ContactDuplicatedException, status
from app.models.contact import GroupTags
from app.schemas.contact import ContactCreate, ContactUpdate
from app.tests.utils.contact import format_phone_number, random_phone_number
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_lower_string


def test_create_contact(db: Session) -> None:
    name = random_lower_string()
    description = random_lower_string()
    phone_number = random_phone_number()
    email = "what@ever.com"
    group_tag = GroupTags.PERSONAL

    contact_in = ContactCreate(
        name=name,
        description=description,
        phone_number=phone_number,
        email=email,
        group_tag=group_tag,
        id=id,
    )

    user = create_random_user(db)

    contact = crud.contact.create_with_owner(db=db, obj_in=contact_in, owner_id=user.id)

    assert contact.name == name
    assert contact.description == description
    assert contact.email == email
    assert contact.deleted is False
    assert contact.group_tag == group_tag
    assert contact.owner_id == user.id


def test_get_contact(db: Session) -> None:
    name = random_lower_string()
    description = random_lower_string()
    phone_number = random_phone_number()
    email = "what@ever.com"
    group_tag = GroupTags.ACADEMIC

    contact_in = ContactCreate(
        name=name,
        description=description,
        phone_number=phone_number,
        email=email,
        group_tag=group_tag,
        id=id,
    )

    user = create_random_user(db)
    contact = crud.contact.create_with_owner(db=db, obj_in=contact_in, owner_id=user.id)
    stored_contact = crud.contact.get(db=db, id=contact.id)

    assert stored_contact
    assert contact.id == stored_contact.id
    assert contact.name == stored_contact.name
    assert contact.description == stored_contact.description
    assert contact.owner_id == stored_contact.owner_id


def test_create_contact_with_same_phone_number(db: Session) -> None:
    phone_number = "48932148976"
    user = create_random_user(db)

    _ = crud.contact.create_with_owner(
        db=db,
        obj_in=ContactCreate(name="John Doe", phone_number=phone_number, id=id,),
        owner_id=user.id,
    )

    with pytest.raises(Exception) as exc:
        _ = crud.contact.create_with_owner(
            db=db,
            obj_in=ContactCreate(
                name="Alana Diestl-Schneider", phone_number=phone_number, id=id,
            ),
            owner_id=user.id,
        )

    assert exc is not None
    assert isinstance(exc.value, ContactDuplicatedException)

    assert exc.value.status_code == status.HTTP_400_BAD_REQUEST
    assert exc.value.detail == {
        "error": "ContactDuplicatedException",
        "message": f"A contact with the phone number {format_phone_number(phone_number)} already exists",
    }


def test_update_contact(db: Session) -> None:
    name = random_lower_string()
    description = random_lower_string()
    phone_number = random_phone_number()

    contact_in = ContactCreate(
        name=name, description=description, phone_number=phone_number, id=id,
    )

    user = create_random_user(db)
    contact = crud.contact.create_with_owner(db=db, obj_in=contact_in, owner_id=user.id)

    new_phone_number = random_phone_number()
    new_name = "John Doe"
    new_tag = GroupTags.ACADEMIC
    new_email = "foo@bar.com"

    updated_contact = crud.contact.update(
        db=db,
        db_obj=contact,
        obj_in=ContactUpdate(
            description=new_phone_number,
            name=new_name,
            group_tag=new_tag,
            email=new_email,
        ),
    )

    assert contact.id == updated_contact.id
    assert contact.name == updated_contact.name
    assert contact.phone_number == updated_contact.phone_number
    assert contact.group_tag == updated_contact.group_tag
    assert contact.owner_id == updated_contact.owner_id


def test_delete_contact(db: Session) -> None:
    name = random_lower_string()
    description = random_lower_string()
    phone_number = random_phone_number()

    contact_in = ContactCreate(
        name=name, description=description, phone_number=phone_number, id=id,
    )

    user = create_random_user(db)

    contact = crud.contact.create_with_owner(db=db, obj_in=contact_in, owner_id=user.id)

    removed_contact = crud.contact.remove(db=db, id=contact.id)

    assert removed_contact is not None
    assert removed_contact.deleted is True
    assert removed_contact.name == contact.name
    assert removed_contact.description == description
    assert removed_contact.phone_number == format_phone_number(phone_number)

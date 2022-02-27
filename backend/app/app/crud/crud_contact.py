from enum import Enum
from typing import Any, Dict, List, Union

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.api.api_v1.exceptions.contacts import ContactDuplicatedException
from app.crud.base import CRUDBase
from app.models.contact import Contact
from app.schemas.contact import ContactCreate, ContactUpdate


class PhoneCheckingAction(str, Enum):
    CREATE = ("create",)
    UPDATE = ("update",)


class CRUDContact(CRUDBase[Contact, ContactCreate, ContactUpdate]):
    def __phone_exists(
        self, db: Session, data: Dict[str, Any], action: PhoneCheckingAction
    ) -> bool:
        """
        Here, the duplicity of phone numbers is checked.
        """
        contact: Union[Contact, List[Contact], None]

        if data.get("phone_number"):
            phone_number = data["phone_number"]
            contact = (
                db.query(self.model)
                .filter(Contact.phone_number == phone_number)
                .first()
            )

            if contact and action == PhoneCheckingAction.UPDATE:
                return contact.phone_number == phone_number

        return contact is not None if action == PhoneCheckingAction.CREATE else False

    def create_with_owner(
        self, db: Session, *, obj_in: ContactCreate, owner_id: int
    ) -> Union[Contact, None]:
        """
        Creation method with phone number verification.
        """
        obj_in_data = jsonable_encoder(obj_in)

        if self.__phone_exists(db, obj_in_data, PhoneCheckingAction.CREATE):
            raise ContactDuplicatedException(obj_in_data["phone_number"])

        db_obj = self.model(**obj_in_data, owner_id=owner_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        return db_obj

    def get_multi_by_owner(
        self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100
    ) -> List[Contact]:
        return (
            db.query(self.model)
            .filter(Contact.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def update(
        self,
        db: Session,
        *,
        db_obj: Contact,
        obj_in: Union[ContactUpdate, Dict[str, Any]],
    ) -> Union[Contact, None]:
        """
        Overriding of the base update method with phone number checking.
        """
        data = jsonable_encoder(obj_in)

        if self.__phone_exists(db, data, PhoneCheckingAction.UPDATE):
            raise ContactDuplicatedException(data["phone_number"])

        return super().update(db, db_obj=db_obj, obj_in=obj_in)

    def remove(self, db: Session, *, id: int) -> Contact:
        """
        Overriding of the base remove method.
        Ensures that the contact record stays in the DB,
        setting the field "deleted" to True.
        """
        contact = db.query(self.model).get(id)
        contact.deleted = True

        db.add(contact)
        db.commit()
        db.refresh(contact)

        return contact


contact = CRUDContact(Contact)

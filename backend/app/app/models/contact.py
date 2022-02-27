from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, TypeDecorator
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .user import User  # noqa: F401


class GroupTags(str, Enum):
    ACADEMIC = "academic"
    PERSONAL = "personal"
    PROFESSIONAL = "professional"
    UNDEFINED = "undefined"


class StrEnumType(TypeDecorator):
    """
    Enables passing in a Python enum and storing the enum's *value* in the db.
    The default would have stored the enum's *name* (ie the string).
    """

    impl = String

    def __init__(self, enumtype, *args, **kwargs):
        super(StrEnumType, self).__init__(*args, **kwargs)
        self._enumtype = enumtype

    def process_bind_param(self, value, dialect):
        if isinstance(value, int):
            return value

        # return value.value
        return value

    def process_result_value(self, value, dialect):
        return self._enumtype(value)


class Contact(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    phone_number = Column(String, index=True, nullable=False)
    email = Column(String, index=True)
    deleted = Column(Boolean, nullable=False, default=False)
    owner_id = Column(Integer, ForeignKey("user.id"))
    group_tag = Column(StrEnumType(GroupTags), default=GroupTags.UNDEFINED)
    owner = relationship("User", back_populates="contacts")

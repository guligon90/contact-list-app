from .crud_contact import contact
from .crud_user import user

# For a new basic set of CRUD operations you could just do

# from .base import CRUDBase
# from app.models.contact import Contact
# from app.schemas.contact import ContactCreate, ContactUpdate

# contact = CRUDBase[Contact, ContactCreate, ContactUpdate](Contact)

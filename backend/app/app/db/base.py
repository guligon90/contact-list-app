# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.base_class import Base  # noqa
from app.models.contact import Contact  # noqa
# from backend.app.app.models.contact import Contact  # noqa
from app.models.user import User  # noqa

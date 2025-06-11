from sqlmodel import Session, SQLModel, create_engine

from base import settings

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))


def init_db(session: Session) -> None:
    """Initialise the database tables."""

    # SQLModel collects metadata for all model classes. Calling ``create_all``
    # will create any tables that do not already exist.
    SQLModel.metadata.create_all(engine)

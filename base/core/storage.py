from sqlmodel import Session, create_engine

from base import settings

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))


def init_db(session: Session):
    pass

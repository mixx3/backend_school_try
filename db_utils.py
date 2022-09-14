from sqlalchemy import create_engine

from engine.settings import get_settings
from engine.models.base import Base


def create_tables():
    engine = create_engine(get_settings().DB_DSN)
    Base.metadata.create_all(engine)


def drop_tables():
    engine = create_engine(get_settings().DB_DSN)
    Base.metadata.drop_all(engine)


if __name__ == '__main__':
    create_tables()

from .base import Base
from datetime import datetime
from sqlalchemy import Column
import sqlalchemy.orm
import enum


class Type(str, enum.Enum):
    FOLDER: str = "FOLDER"
    FILE: str = "FILE"


class FileInfo(Base):
    id = Column(sqlalchemy.String, nullable=False)
    parentId = Column(sqlalchemy.String, nullable=True)
    type = Column(sqlalchemy.String, nullable=False)
    url = Column(sqlalchemy.String, nullable=True)
    size = Column(sqlalchemy.Integer, nullable=True)




from .base import Base
from datetime import datetime
from sqlalchemy import Column
import sqlalchemy.orm
import enum


class Type(str, enum.Enum):
    FOLDER: str = "FOLDER"
    FILE: str = "FILE"


class FileInfo(Base):
    file_id = Column(sqlalchemy.Integer, nullable=False, primary_key=True)
    id = Column(sqlalchemy.String, nullable=False)
    date = Column(sqlalchemy.DateTime, nullable=False)
    type = Column(sqlalchemy.String, nullable=False)
    parentId = Column(sqlalchemy.String, nullable=True)
    url = Column(sqlalchemy.String, nullable=True)
    size = Column(sqlalchemy.Integer, nullable=True)

    def __repr__(self):
        return f"FileInfo(id: {self.id}, date: {self.date}"

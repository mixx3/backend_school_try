from pydantic import BaseModel
from datetime import datetime


class SystemChunk(BaseModel):
    id: str
    date: datetime
    type: str
    parentId: str | None
    url: str | None
    size: int | None


class ImportBatch(BaseModel):
    items: list[SystemChunk]
    updateDate: datetime


class SystemItem(BaseModel):
    id: str
    date: datetime
    type: str
    parentId: str | None
    url: str | None
    size: int | None
    children: list[SystemChunk]


class Error(BaseModel):
    code: int
    message: str

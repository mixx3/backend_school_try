from pydantic import BaseModel
from datetime import datetime


class ImportBatch(BaseModel):
    items: list[ImportChunk]
    updateDate: datetime


class ImportChunk(BaseModel):
    id: str
    date: str
    type: str
    parentId: str | None
    url: str | None
    size: int | None

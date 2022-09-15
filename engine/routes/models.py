from pydantic import BaseModel
from datetime import datetime
from engine.models.db import Type


from datetime import datetime, timezone
from pydantic import BaseModel, validator


def convert_datetime_to_iso_8601_with_z_suffix(dt: datetime) -> str:
    return dt.strftime('%Y-%m-%dT%H:%M:%SZ')


def transform_to_utc_datetime(dt: datetime) -> datetime:
    return dt.astimezone(tz=timezone.utc)


class DateTimeSpecial(BaseModel):
    datetime_in_utc_with_z_suffix: datetime

    # custom input conversion for that field
    _normalize_datetimes = validator(
        "datetime_in_utc_with_z_suffix",
        allow_reuse=True)(transform_to_utc_datetime)

    class Config:
        json_encoders = {
            # custom output conversion for datetime
            datetime: convert_datetime_to_iso_8601_with_z_suffix
        }


class SystemChunk(BaseModel):
    id: str
    date: str
    type: Type
    parentId: str | None = None
    url: str | None
    size: int | None


class ImportChunk(BaseModel):
    id: str
    date: DateTimeSpecial | None
    type: Type
    parentId: str | None
    url: str | None
    size: int | None


class ImportBatch(BaseModel):
    items: list[ImportChunk]
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

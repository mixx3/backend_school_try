import json

from engine.settings import get_settings
from engine.routes.models import SystemChunk, SystemItem
from engine.models.db import FileInfo
from engine.models.base import AlchemyEncoder
from sqlalchemy.orm import Session
from logging import getLogger
from engine.exceptions import NodeNotFound
from datetime import datetime


logger = getLogger(__name__)


async def add_system_item(item: SystemChunk, session: Session) -> None:
    logger.debug(f"Adding {item.id} to db...")
    session.add(FileInfo(**item.dict()))
    session.flush()


async def get_children_by_id(id: str, session: Session) -> list[FileInfo]:
    return session.query(FileInfo).filter(FileInfo.parentId == id).all()


async def get_node_by_id(id: str, session: Session) -> SystemItem:
    node: FileInfo = session.query(FileInfo).filter(FileInfo.id == id).one_or_none()
    if not node:
        raise NodeNotFound(id)
    children = []
    for child in await get_children_by_id(id, session):
        children.append(SystemChunk(**dict(json.dumps(child, cls=AlchemyEncoder))))
    return SystemItem(**dict(json.dumps(node, cls=AlchemyEncoder)), children=children)


async def delete_node_by_id(id: str, session: Session) -> None:
    node: SystemChunk = session.query(FileInfo).filter(FileInfo.id == id).one_or_none()
    if not node:
        raise NodeNotFound(id)
    children = await get_children_by_id(id, session)
    session.delete(node)
    for child in children:
        session.delete(child)


async def get_nodes_by_date(session: Session,
                            id: str | None = None,
                            start_date: datetime | None = None,
                            end_date: datetime | None = None) -> list[FileInfo]:
    if not id:
        res = session.query(FileInfo).filter(start_date <= FileInfo.date,
                                             FileInfo.date <= end_date).all()
    else:
        if not start_date and not end_date:
            res = session.query(FileInfo).filter(FileInfo.id == id).all()
        else:
            res = session.query(FileInfo).filter(FileInfo.id == id,
                                                 start_date <= FileInfo.date,
                                                 FileInfo.date <= end_date).all()
        if not res:
            raise NodeNotFound(id)
    return res

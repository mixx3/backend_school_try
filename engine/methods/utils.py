import json
from typing import Dict, Any, List

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
    res = session.query(FileInfo).filter(FileInfo.parentId == id).all()
    session.flush()
    return res


async def get_node_by_id(id: str, session: Session) -> dict[Any, list[SystemChunk] | Any]:
    nodes: list[FileInfo] = session.query(FileInfo).filter(FileInfo.id == id).all()
    session.flush()
    if not nodes:
        raise NodeNotFound(id)
    children = []
    node = nodes[0]
    n = node.to_dict()
    n['date'] = str(n['date'])
    for child in await get_children_by_id(id, session):
        c = child.to_dict()
        c['date'] = str(c['date'])
        children.append(c)
    return dict(**n, children=children)


async def delete_node_by_id(id: str, session: Session) -> None:
    nodes: list[FileInfo] = session.query(FileInfo).filter(FileInfo.id == id).all()
    session.flush()
    if not nodes:
        raise NodeNotFound(id)
    children = await get_children_by_id(id, session)
    for node in nodes:
        session.delete(node)
    session.flush()
    if children:
        for child in children:
            session.delete(child)
            session.flush()


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
    session.flush()
    return res

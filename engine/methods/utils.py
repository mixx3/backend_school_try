import json
from typing import Dict, Any, List
from collections import deque
from engine.settings import get_settings
from engine.routes.models import SystemChunk, SystemItem
from engine.models.db import FileInfo
from engine.models.base import AlchemyEncoder
from sqlalchemy.orm import Session
from logging import getLogger
from engine.exceptions import NodeNotFound
from datetime import datetime
from engine.models.db import Type

logger = getLogger(__name__)


async def add_system_item(item: SystemChunk, session: Session) -> None:
    """
    Add SystemChunk to DB table file_info
    :param item: SystemChunk obj
    :param session: sqlalchemy session (ex. fastapi_sqlalchemy.db.session)
    :return: None
    """
    logger.debug(f"Adding {item.id} to db...")
    session.add(FileInfo(**item.dict()))
    session.flush()


async def get_children_by_id(id: str, session: Session) -> list[FileInfo]:
    """
    DB get children. Returns all children, not recent
    :param id: node id
    :param session: db session
    :return: list of FileInfo objects
    """
    logger.debug(f"Getting children for node id: {id}")
    res = session.query(FileInfo).filter(FileInfo.parentId == id).all()
    session.flush()
    return res


async def find_latest_node(nodes: list[FileInfo]) -> dict:
    """
    Find latest_node (recent update of node)
    :param nodes: list of nodes (expected that all nodes have the same id, else function makes no sense)
    :return: dict(SystemChunk - like dict)
    """
    logger.debug(f"Finding last update for node...")
    res = [n.to_dict() for n in nodes]
    return sorted(res, key=lambda n: n['date'])[-1]


async def find_children(node: dict, id: str, session: Session) -> None:
    """
    Find children for node with id (id)
    :param node: dict(SystemChunk - like dict)
    :param id: node id (or child id in recursion)
    :param session: db session
    :return: None
    """
    logger.debug(f"Finding children for node")
    if node['type'] == Type.FOLDER:
        node['children'] = []
        children_with_history = await get_children_by_id(id, session)
        children_ids = set()
        for c in children_with_history:
            children_ids.add(c.to_dict()['id'])
        for i in children_ids:
            child = await find_latest_node(session.query(FileInfo).filter(FileInfo.id == i).all())
            if child:
                split_date = str(child['date']).split()
                child['date'] = f"{split_date[0]}T{split_date[1]}Z"
                node['children'].append(child)
                node['size'] += child.get('size', 0)
                await find_children(child, child['id'], session)
    else:
        node['children'] = None


async def get_node_by_id(id: str, session: Session) -> dict[Any, list[SystemChunk] | Any]:
    logger.debug(f"Getting node by id: {id}")
    nodes: list[FileInfo] = session.query(FileInfo).filter(FileInfo.id == id).all()
    session.flush()
    if not nodes:
        logger.info(f"Node with id {id} not found in db")
        raise NodeNotFound(id)
    node = await find_latest_node(nodes)
    split_date = str(child['date']).split()
    node['date'] = f"{split_date[0]}T{split_date[1]}Z"
    await find_children(node, id, session)
    return node


async def delete_node_by_id(id: str, session: Session) -> None:
    """
    Deletes all nodes with given id
    :param id: node id (str)
    :param session: db session
    :return: None
    """
    logger.debug(f"Deleting node with id: {id}")
    nodes: list[FileInfo] = session.query(FileInfo).filter(FileInfo.id == id).all()
    session.flush()
    if not nodes:
        logger.info(f"Node with id {id} not found in db")
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
    """
    Get nodes with start_date <= date <= end_date and id == given id
    :param session: db session
    :return: list[FileInfo]
    """
    if not id:
        res = session.query(FileInfo).filter(start_date <= FileInfo.date,
                                             FileInfo.date <= end_date).all()
        logger.debug(f"Getting all nodes from {start_date} to {end_date}")
    else:
        if not start_date and not end_date:
            res = session.query(FileInfo).filter(FileInfo.id == id).all()
            logger.debug(f"Getting all nodes with id {id}")
        else:
            res = session.query(FileInfo).filter(FileInfo.id == id,
                                                 start_date <= FileInfo.date,
                                                 FileInfo.date <= end_date).all()
            logger.debug(f"Getting all nodes from {start_date} to {end_date} with id {id}")
        if not res:
            logger.info(f"Node with id {id} not found in db")
            raise NodeNotFound(id)
    session.flush()
    return res

from datetime import datetime
from fastapi import APIRouter, Path, Query
from logging import getLogger
from engine.methods.utils import get_node_by_id, delete_node_by_id, get_nodes_by_date
from engine.models.base import AlchemyEncoder
from fastapi.responses import JSONResponse
from fastapi_sqlalchemy import db
import json


node_router = APIRouter(tags=["nodes", "updates"])
logger = getLogger(__name__)


@node_router.get("/nodes/{id}")
async def get_nodes(id: str = Path()):
    logger.debug(f"Getting node with id: {id}")
    db_res = await get_node_by_id(id, db.session)
    res = []
    for node in db_res:
        res.append(json.dumps(node, cls=AlchemyEncoder))
    return JSONResponse(status_code=200, content=res)


@node_router.get("/node/{id}/history")
async def get_node_history(id: str = Path(title='id элемента для которого будет отображаться история'),
                           dateStart: datetime | None = Query(title='Дата и время начала интервала, для которого считается история.' ,default=None),
                           dateEnd: datetime | None = Query(title='Дата и время конца интервала, для которого считается история.', default=None)):
    logger.debug(f"Getting node history id: {id}, dateStart: {dateStart}, dateEnd: {dateEnd}")
    db_res = await get_nodes_by_date(db.session, start_date=dateStart, end_date=dateEnd, id=id)
    res = []
    for node in db_res:
        res.append(json.dumps(node, cls=AlchemyEncoder))
    return JSONResponse(status_code=200, content=res)


@node_router.get("/delete/{id}")
async def delete_node(id: str):
    logger.debug(f"Deleting node with id: {id}")
    await delete_node_by_id(id, db.session)
    return JSONResponse(status_code=200,
                        content={'description': 'Удаление прошло успешно.'}
                        )

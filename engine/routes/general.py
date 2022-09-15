import json
from datetime import datetime, timedelta
from fastapi import APIRouter
from logging import getLogger
from .models import ImportBatch, SystemChunk
from fastapi_sqlalchemy import db
from engine.methods.utils import add_system_item, get_nodes_by_date
from fastapi.responses import JSONResponse
from engine.models.base import AlchemyEncoder

general_router = APIRouter()
logger = getLogger(__name__)


@general_router.post("/imports")
async def create_nodes(batch: ImportBatch):
    logger.debug("creating nodes")
    items = batch.items
    upd_time = batch.updateDate
    for item in items:
        item.date = upd_time
        await add_system_item(item, db.session)
    res = json.dumps({'description': 'Вставка или обновление прошли успешно.'}, ensure_ascii=True)
    return JSONResponse(res, status_code=200, )


@general_router.get("/updates")
async def get_updates(date: datetime):
    delta = timedelta(days=1)
    start_date = date - delta
    logger.debug(f"Checking nodes for update in time interval: [{start_date} : {date}]")
    nodes = await get_nodes_by_date(db.session, start_date=start_date, end_date=date)
    res = []
    for node in nodes:
        res.append(json.dumps(node, cls=AlchemyEncoder))
    return JSONResponse(res, status_code=200)

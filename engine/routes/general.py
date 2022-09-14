from fastapi import APIRouter
from logging import getLogger


general_router = APIRouter()
gen_router = getLogger(__name__)


@general_router.post("/imports")
async def create_node():
    pass


@general_router.get("/updates")
async def get_updates():
    pass

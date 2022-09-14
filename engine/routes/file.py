from fastapi import APIRouter
from logging import getLogger


node_router = APIRouter(tags=["nodes", "updates"])
node_logger = getLogger(__name__)


@node_router.get("/nodes/{id}")
async def get_nodes():
    pass


@node_router.get("/node/{id}/history")
async def get_node_history():
    pass


@node_router.get("/delete/{id}")
async def delete_node():
    pass



from fastapi import APIRouter


file_router = APIRouter(tags=["nodes", "updates"])


@file_router.get("/nodes/{id}")
async def get_nodes():
    pass


@file_router.get("/node/{id}/history")
async def get_node_hostory():
    pass


@file_router.get("/delete/{id}")
async def delete_node():
    pass



from fastapi import APIRouter

general_router = APIRouter()


@general_router.post("/imports")
async def create_node():
    pass


@general_router.get("/updates")
async def get_updates():
    pass

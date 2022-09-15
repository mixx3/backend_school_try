from fastapi import FastAPI
from .general import general_router
from .node import node_router
from engine.settings import get_settings
from fastapi_sqlalchemy import DBSessionMiddleware
from engine.exceptions import NodeNotFound
from fastapi.responses import JSONResponse
from logging import getLogger
import starlette


app = FastAPI()
settings = get_settings()
logger = getLogger(__name__)

app.add_middleware(
    DBSessionMiddleware,
    db_url=settings.DB_DSN,
    session_args={"autocommit": True},
)


app.include_router(general_router)
app.include_router(node_router)


@app.exception_handler(NodeNotFound)
async def not_found_error(request: starlette.requests.Request, exc: NodeNotFound):
    return JSONResponse({"error": exc.args[0], "request": request.path_params}, status_code=404)


@app.exception_handler(ValueError)
async def http_value_error_handler(request: starlette.requests.Request, exc: ValueError):
    logger.info(f"Failed to parse data, request: {request.path_params}, exc: {exc}")
    return JSONResponse({"error": "Error"}, status_code=400)

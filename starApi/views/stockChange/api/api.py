import time
import json
import hashlib
import asyncio
import aiohttp

from fastapi import *
from fastapi.routing import APIRouter
from fastapi.responses import ORJSONResponse, JSONResponse
from fastapi.responses import StreamingResponse
from loguru import logger
from utils.tools.index import *
from utils.ticket.request.api import *

ReqClient = RequestClient()

router = APIRouter(
    prefix="/api",
    tags=["异动"],
    default_response_class=ORJSONResponse
)


_time = 0.03

@router.get("/change")
async def stock_change(request: Request):
    data = await ReqClient.stock_change()
    return JSONResponse(status_code=200, content=data)


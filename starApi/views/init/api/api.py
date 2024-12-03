from fastapi import *
from fastapi.routing import APIRouter
from fastapi.responses import ORJSONResponse, JSONResponse

from utils.ticket.request.api import *

ReqClient = RequestClient()

router = APIRouter(
    prefix="/api",
    tags=["初始数据"],
    default_response_class=ORJSONResponse
)


@router.get("/init/station")
async def init_station():
    data = ReqClient.station()
    return JSONResponse(status_code=200, content=data)

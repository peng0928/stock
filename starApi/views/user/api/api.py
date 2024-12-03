from utils.ticket.request.api import *

from utils.ticket.request.tool.ticket_tool import request_set_cookie
from fastapi.responses import ORJSONResponse, JSONResponse
from fastapi.routing import APIRouter
from fastapi import *

ReqClient = RequestClient()

router = APIRouter(
    prefix="/api",
    tags=["user"],
    default_response_class=ORJSONResponse
)


@router.post("/conf")
async def conf(request: Request):
    data = ReqClient.get_conf(cookie=request.cookies)
    return JSONResponse(status_code=200, content=data)



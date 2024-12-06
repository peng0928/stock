import time
import hashlib

from fastapi import *
from fastapi.routing import APIRouter
from fastapi.responses import ORJSONResponse, JSONResponse
from fastapi.responses import StreamingResponse

from utils.ticket.request.api import *
from views.stock.model.index import *

ReqClient = RequestClient()

router = APIRouter(
    prefix="/api",
    tags=["订单"],
    default_response_class=ORJSONResponse
)


@router.post("/stock/get")
async def stock_get(request: Request, item: StockItem):
    data = ReqClient.stock_get(code=item.code)
    return JSONResponse(status_code=200, content=data)


@router.post("/stock/trend")
async def stock_trend(request: Request, item: StockTrend):
    hy = item.hy
    dp = item.dp
    code = item.code
    data = []
    hy_data = ReqClient.stock_trends2(code=hy)
    dp_data = ReqClient.stock_trends2(code=dp)
    if hy_data:
        data.append(hy_data)
    if dp_data:
        data.append(dp_data)
    bk_data = ReqClient.stock_securities(code=code)
    if bk_data:
        for item in bk_data:
            data.append(item)
    return JSONResponse(status_code=200, content=data)


@router.post("/stock/trend/data")
async def stock_trend_data(request: Request, item: StockItem):
    code = item.code
    data = ReqClient.stock_trends(code=code)
    return JSONResponse(status_code=200, content=data)


@router.post("/stock/details")
async def stock_trend_data(request: Request, item: StockItem):
    code = item.code
    data = ReqClient.stock_details(code=code)
    return JSONResponse(status_code=200, content=data)


# SSE生成器，用于向客户端发送事件流
async def event_generator(request: Request):
    md5_code = ""
    while True:
        if await request.is_disconnected():
            logger.info("连接已中断")
            break

        data = ReqClient.stock_zs()
        new_md5_code = hashlib.md5(str(data).encode()).hexdigest()
        if md5_code != new_md5_code:
            md5_code = new_md5_code
            yield f"data: {data}\n\n"
        time.sleep(1)


# SSE endpoint，用于客户端连接
@router.get("/stock/zs")
async def stock_zs(request: Request):
    # 返回SSE流
    return StreamingResponse(event_generator(request), media_type="text/event-stream")

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

sse_time = 0.614
media_type = "text/event-stream"


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


@router.get("/stock/get/{item}")
async def stock_get_sse(request: Request, item):
    return StreamingResponse(event_generator(request, 'stock_get', code=item), media_type=media_type)


@router.get("/stock/trend")
async def stock_trend_sse(request: Request, hy, dp, code):
    return StreamingResponse(event_generator(request, 'trend_data', hy=hy, dp=dp, code=code, stime=3),
                             media_type=media_type)


@router.get("/stock/trend/data/{item}")
async def stock_trend_data_sse(request: Request, item):
    return StreamingResponse(event_generator(request, 'stock_trends', code=item), media_type=media_type)


@router.post("/stock/details")
async def stock_trend_details(request: Request, item: StockItem):
    code = item.code
    data = ReqClient.stock_details(code=code)
    return JSONResponse(status_code=200, content=data)


@router.post("/stock/bk")
async def stock_bk(request: Request, ):
    data = ReqClient.stock_bk()
    return JSONResponse(status_code=200, content=data)


@router.post("/stock/ztb")  # 涨停板
async def stock_ztb(request: Request ):
    data = ReqClient.stock_ZTPool()
    return JSONResponse(status_code=200, content=data)


# SSE生成器，用于向客户端发送事件流
async def event_generator(request: Request, func="", stime='', **kwargs):
    md5_code = ""
    stime = stime if stime else sse_time
    event_func = {
        "stock_zs": ReqClient.stock_zs,
        "stock_get": ReqClient.stock_get,
        "stock_trends": ReqClient.stock_trends,
        "trend_data": trend_data,
    }
    while True:
        data = event_func.get(func)(**kwargs)
        if isinstance(data, dict) or isinstance(data, list):
            data = json.dumps(data)
        new_md5_code = hashlib.md5(str(data).encode()).hexdigest()
        if md5_code != new_md5_code:
            md5_code = new_md5_code
            yield f"data: {data}\n\n"
        else:
            time.sleep(stime)
        if await request.is_disconnected():
            logger.info("连接已中断")
            break


# SSE endpoint，用于客户端连接
@router.get("/stock/zs")
async def stock_zs(request: Request):
    # 返回SSE流
    return StreamingResponse(event_generator(request, 'stock_zs'), media_type=media_type)


def trend_data(hy, dp, code):
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
    return data
